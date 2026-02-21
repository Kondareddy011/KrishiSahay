"""
Database manager - Supabase (primary) with MySQL fallback.
Stores cache, feedback, and image analysis.
"""

import os
import json
from datetime import datetime
from typing import Optional, Dict, Any, List

from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(env_path)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))


def _get_mongodb_client():
    """Create MongoDB client if configured."""
    uri = os.getenv("MONGODB_URI")
    db_name = os.getenv("MONGODB_DB", "krishisahay")
    if not uri:
        return None
    try:
        from pymongo import MongoClient
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        # Verify connection
        client.server_info()
        return client[db_name]
    except Exception as e:
        print(f"MongoDB init error: {e}")
        return None


def _get_supabase_client():
    """Create Supabase client if credentials exist."""
    url = os.getenv("SUPABASE_URL") or os.getenv("VITE_SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_ANON_KEY") or os.getenv("VITE_SUPABASE_ANON_KEY")
    if not url or not key:
        return None
    try:
        from supabase import create_client
        return create_client(url, key)
    except Exception as e:
        print(f"Supabase init error: {e}")
        return None


def _get_mysql_conn():
    """Create MySQL connection if configured."""
    try:
        import pymysql
        host = os.getenv("MYSQL_HOST", "localhost")
        port = int(os.getenv("MYSQL_PORT", "3306"))
        user = os.getenv("MYSQL_USER", "root")
        password = os.getenv("MYSQL_PASSWORD", "")
        db_name = os.getenv("MYSQL_DB", "krishisahay")
        if not password and not host:
            return None
        return pymysql.connect(
            host=host, port=port, user=user, password=password, database=db_name,
            cursorclass=pymysql.cursors.DictCursor, autocommit=True,
        )
    except Exception as e:
        print(f"MySQL init error: {e}")
        return None


class Database:
    """Uses Supabase first, falls back to MySQL, then no-op."""

    def __init__(self) -> None:
        self.supabase = _get_supabase_client()
        self.mongodb = _get_mongodb_client()
        self.mysql = _get_mysql_conn() if self.supabase is None and self.mongodb is None else None
        
        if self.supabase:
            print("Database: Using Supabase")
        elif self.mongodb is not None:
            print("Database: Using MongoDB")
        elif self.mysql:
            print("Database: Using MySQL")
            self._create_mysql_tables()
        else:
            print("Database: No backend (cache/feedback will not persist)")

    def _create_mysql_tables(self) -> None:
        if not self.mysql:
            return
        try:
            with self.mysql.cursor() as c:
                c.execute("""
                    CREATE TABLE IF NOT EXISTS query_cache (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        query TEXT NOT NULL, query_lower TEXT NOT NULL, language VARCHAR(10) DEFAULT 'en',
                        answer TEXT NOT NULL, category VARCHAR(255), hit_count INT DEFAULT 1,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                        UNIQUE KEY uq_ql (query_lower(255), language)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
                """)
                c.execute("""
                    CREATE TABLE IF NOT EXISTS user_feedback (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        query TEXT NOT NULL, answer TEXT NOT NULL, feedback VARCHAR(20) NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
                """)
                c.execute("""
                    CREATE TABLE IF NOT EXISTS image_analysis (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        image_filename TEXT, analysis_result JSON, language VARCHAR(10) DEFAULT 'en',
                        user_query TEXT, recommendations TEXT NOT NULL, category VARCHAR(255),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
                """)
                c.execute("""
                    CREATE TABLE IF NOT EXISTS app_feedback (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        rating TINYINT NULL, message TEXT NOT NULL, page VARCHAR(50) NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
                """)
        except Exception as e:
            print(f"MySQL tables error: {e}")

    def initialize(self) -> None:
        pass  # Already done in __init__

    def _ensure_supabase_tables(self) -> None:
        """Supabase tables must exist (run migration in dashboard). No-op if tables missing."""
        pass

    def get_cached_response(self, query: str, language: str) -> Optional[Dict[str, Any]]:
        q = query.lower().strip()
        if self.supabase:
            try:
                r = self.supabase.table("query_cache").select("answer, category").eq("query_lower", q).eq("language", language).order("updated_at", desc=True).limit(1).execute()
                if r.data and len(r.data) > 0:
                    return {"answer": r.data[0]["answer"], "category": r.data[0].get("category")}
            except Exception as e:
                print(f"Supabase cache get: {e}")
        if self.mongodb is not None:
            try:
                row = self.mongodb.query_cache.find_one(
                    {"query_lower": q, "language": language},
                    sort=[("updated_at", -1)]
                )
                if row:
                    return {"answer": row["answer"], "category": row.get("category")}
            except Exception as e:
                print(f"MongoDB cache get: {e}")
        if self.mysql:
            try:
                with self.mysql.cursor() as c:
                    c.execute("SELECT answer, category FROM query_cache WHERE query_lower=%s AND language=%s ORDER BY updated_at DESC LIMIT 1", (q, language))
                    row = c.fetchone()
                    if row:
                        return {"answer": row["answer"], "category": row.get("category")}
            except Exception as e:
                print(f"MySQL cache get: {e}")
        return None

    def cache_response(self, query: str, language: str, answer: str, category: Optional[str] = None) -> None:
        q = query.lower().strip()
        now = datetime.now()
        if self.supabase:
            try:
                r = self.supabase.table("query_cache").select("id, hit_count").eq("query_lower", q).eq("language", language).maybe_single().execute()
                if r.data:
                    self.supabase.table("query_cache").update({"answer": answer, "category": category, "hit_count": (r.data.get("hit_count") or 0) + 1, "updated_at": now.isoformat()}).eq("id", r.data["id"]).execute()
                else:
                    self.supabase.table("query_cache").insert({"query": query, "query_lower": q, "language": language, "answer": answer, "category": category, "hit_count": 1}).execute()
            except Exception as e:
                print(f"Supabase cache save: {e}")
        if self.mongodb is not None:
            try:
                self.mongodb.query_cache.update_one(
                    {"query_lower": q, "language": language},
                    {
                        "$set": {
                            "query": query,
                            "answer": answer,
                            "category": category,
                            "updated_at": now
                        },
                        "$inc": {"hit_count": 1},
                        "$setOnInsert": {"created_at": now}
                    },
                    upsert=True
                )
            except Exception as e:
                print(f"MongoDB cache save: {e}")
        if self.mysql:
            try:
                with self.mysql.cursor() as c:
                    c.execute("SELECT id, hit_count FROM query_cache WHERE query_lower=%s AND language=%s LIMIT 1", (q, language))
                    row = c.fetchone()
                    if row:
                        c.execute("UPDATE query_cache SET answer=%s, category=%s, hit_count=hit_count+1, updated_at=%s WHERE id=%s", (answer, category, now.strftime("%Y-%m-%d %H:%M:%S"), row["id"]))
                    else:
                        c.execute("INSERT INTO query_cache (query, query_lower, language, answer, category, hit_count) VALUES (%s,%s,%s,%s,%s,1)", (query, q, language, answer, category))
            except Exception as e:
                print(f"MySQL cache save: {e}")

    def save_feedback(self, query: str, answer: str, feedback: str) -> None:
        if self.supabase:
            try:
                self.supabase.table("user_feedback").insert({"query": query, "answer": answer, "feedback": feedback}).execute()
            except Exception as e:
                print(f"Supabase feedback: {e}")
        if self.mongodb is not None:
            try:
                self.mongodb.user_feedback.insert_one({
                    "query": query,
                    "answer": answer,
                    "feedback": feedback,
                    "created_at": datetime.now()
                })
            except Exception as e:
                print(f"MongoDB feedback: {e}")
        if self.mysql:
            try:
                with self.mysql.cursor() as c:
                    c.execute("INSERT INTO user_feedback (query, answer, feedback) VALUES (%s,%s,%s)", (query, answer, feedback))
            except Exception as e:
                print(f"MySQL feedback: {e}")

    def save_image_analysis(self, image_filename: str, analysis_result: Dict, language: str, user_query: Optional[str], recommendations: str, category: Optional[str]) -> None:
        ar_json = json.dumps(analysis_result, ensure_ascii=False)
        if self.supabase:
            try:
                # Supabase JSONB accepts dict directly
                self.supabase.table("image_analysis").insert({
                    "image_filename": image_filename,
                    "analysis_result": analysis_result,
                    "language": language,
                    "user_query": user_query,
                    "recommendations": recommendations,
                    "category": category,
                }).execute()
            except Exception as e:
                print(f"Supabase image_analysis: {e}")
        if self.mongodb is not None:
            try:
                self.mongodb.image_analysis.insert_one({
                    "image_filename": image_filename,
                    "analysis_result": analysis_result,
                    "language": language,
                    "user_query": user_query,
                    "recommendations": recommendations,
                    "category": category,
                    "created_at": datetime.now()
                })
            except Exception as e:
                print(f"MongoDB image_analysis: {e}")
        if self.mysql:
            try:
                with self.mysql.cursor() as c:
                    c.execute("INSERT INTO image_analysis (image_filename, analysis_result, language, user_query, recommendations, category) VALUES (%s,%s,%s,%s,%s,%s)", (image_filename, ar_json, language, user_query, recommendations, category))
            except Exception as e:
                print(f"MySQL image_analysis: {e}")

    def save_app_feedback(self, message: str, rating: Optional[int] = None, page: Optional[str] = None) -> None:
        if self.supabase:
            try:
                self.supabase.table("app_feedback").insert({"message": message, "rating": rating, "page": page}).execute()
            except Exception as e:
                print(f"Supabase app_feedback: {e}")
        if self.mongodb is not None:
            try:
                self.mongodb.app_feedback.insert_one({
                    "message": message,
                    "rating": rating,
                    "page": page,
                    "created_at": datetime.now()
                })
            except Exception as e:
                print(f"MongoDB app_feedback: {e}")
        if self.mysql:
            try:
                with self.mysql.cursor() as c:
                    c.execute("INSERT INTO app_feedback (message, rating, page) VALUES (%s,%s,%s)", (message, rating, page))
            except Exception as e:
                print(f"MySQL app_feedback: {e}")

    def get_recent_app_feedback(self, limit: int = 20) -> List[Dict[str, Any]]:
        if self.supabase:
            try:
                r = self.supabase.table("app_feedback").select("id, rating, message, page, created_at").order("created_at", desc=True).limit(limit).execute()
                return r.data or []
            except Exception as e:
                print(f"Supabase get app_feedback: {e}")
        if self.mongodb is not None:
            try:
                cursor = self.mongodb.app_feedback.find().sort("created_at", -1).limit(limit)
                results = []
                for doc in cursor:
                    doc["id"] = str(doc.pop("_id"))
                    results.append(doc)
                return results
            except Exception as e:
                print(f"MongoDB get app_feedback: {e}")
        if self.mysql:
            try:
                with self.mysql.cursor() as c:
                    c.execute("SELECT id, rating, message, page, created_at FROM app_feedback ORDER BY created_at DESC LIMIT %s", (limit,))
                    return c.fetchall() or []
            except Exception as e:
                print(f"MySQL get app_feedback: {e}")
        return []

    def is_connected(self) -> bool:
        return self.supabase is not None or self.mongodb is not None or self.mysql is not None

    def close(self) -> None:
        if self.mysql:
            try:
                self.mysql.close()
            except Exception:
                pass
            self.mysql = None
        self.supabase = None
        self.mongodb = None
