import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "npm:@supabase/supabase-js@2";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Client-Info, Apikey",
};

interface QueryRequest {
  query: string;
  language?: string;
}

interface QueryResponse {
  answer: string;
  source: string;
  category?: string;
}

const translations: Record<string, Record<string, string>> = {
  te: {
    "crop": "పంట",
    "pest": "తెగులు",
    "fertilizer": "ఎరువులు",
    "scheme": "పథకం",
    "weather": "వాతావరణం",
  },
  hi: {
    "crop": "फसल",
    "pest": "कीट",
    "fertilizer": "उर्वरक",
    "scheme": "योजना",
    "weather": "मौसम",
  }
};

function detectCategory(query: string): string {
  const lowerQuery = query.toLowerCase();

  if (lowerQuery.match(/crop|plant|grow|seed|harvest|paddy|wheat|rice|cotton|maize/)) {
    return "crops";
  }
  if (lowerQuery.match(/pest|insect|bug|disease|infection|fungus|worm/)) {
    return "pests";
  }
  if (lowerQuery.match(/fertilizer|nutrient|npk|urea|compost|manure/)) {
    return "fertilizers";
  }
  if (lowerQuery.match(/scheme|subsidy|loan|government|pm|kisan|policy/)) {
    return "schemes";
  }
  if (lowerQuery.match(/weather|rain|drought|temperature|climate|season/)) {
    return "weather";
  }

  return "general";
}

function generateContextualAnswer(query: string, category: string, knowledge: any[]): string {
  if (knowledge.length === 0) {
    return generateDefaultAnswer(query, category);
  }

  const relevantInfo = knowledge.slice(0, 3);
  let answer = "";

  switch (category) {
    case "crops":
      answer = `Based on agricultural best practices:\n\n`;
      answer += relevantInfo.map((k, i) => `${i + 1}. ${k.title}: ${k.content.substring(0, 200)}...`).join("\n\n");
      break;
    case "pests":
      answer = `Pest Management Recommendations:\n\n`;
      answer += relevantInfo.map((k, i) => `${i + 1}. ${k.title}: ${k.content.substring(0, 200)}...`).join("\n\n");
      break;
    case "fertilizers":
      answer = `Fertilizer Application Guidelines:\n\n`;
      answer += relevantInfo.map((k, i) => `${i + 1}. ${k.title}: ${k.content.substring(0, 200)}...`).join("\n\n");
      break;
    case "schemes":
      answer = `Government Schemes Information:\n\n`;
      answer += relevantInfo.map((k, i) => `${i + 1}. ${k.title}: ${k.content.substring(0, 200)}...`).join("\n\n");
      break;
    default:
      answer = generateDefaultAnswer(query, category);
  }

  return answer;
}

function generateDefaultAnswer(query: string, category: string): string {
  const responses: Record<string, string> = {
    crops: `For crop-related queries, here are general recommendations:

1. Soil Preparation: Ensure proper soil testing before planting
2. Seed Selection: Use certified seeds from authorized dealers
3. Water Management: Maintain optimal moisture levels
4. Pest Monitoring: Regular inspection for early detection

For specific advice, please consult your local agricultural extension officer.`,

    pests: `For pest management:

1. Identification: First, identify the pest correctly
2. Integrated Pest Management (IPM): Use biological control methods first
3. Chemical Control: Use pesticides only as a last resort
4. Dosage: Always follow recommended dosages

Safety: Wear protective equipment when applying pesticides.`,

    fertilizers: `Fertilizer Application Guidelines:

1. Soil Testing: Get soil tested to know nutrient levels
2. NPK Balance: Apply balanced NPK based on crop requirements
3. Organic Matter: Use compost and farmyard manure
4. Timing: Apply at the right growth stages

Note: Over-fertilization can harm crops and soil health.`,

    schemes: `Government Agricultural Schemes:

1. PM-KISAN: Direct income support to farmers
2. Crop Insurance: PMFBY for crop risk protection
3. KCC: Kisan Credit Card for financial support
4. Soil Health Card: Free soil testing

Visit your nearest Krishi Vigyan Kendra for more information.`,

    weather: `Weather-Based Farming Tips:

1. Monsoon: Plan sowing according to monsoon forecast
2. Drought: Use drought-resistant varieties
3. Cold: Protect sensitive crops from frost
4. Heat: Ensure adequate irrigation during hot weather

Check local weather forecasts regularly.`,

    general: `Agricultural Best Practices:

1. Crop Rotation: Change crops each season
2. Soil Health: Maintain organic matter in soil
3. Water Conservation: Use drip or sprinkler irrigation
4. Record Keeping: Maintain farm records for better planning

For specific guidance, contact your local agricultural department.`
  };

  return responses[category] || responses.general;
}

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") {
    return new Response(null, {
      status: 200,
      headers: corsHeaders,
    });
  }

  try {
    const supabase = createClient(
      Deno.env.get("SUPABASE_URL") ?? "",
      Deno.env.get("SUPABASE_ANON_KEY") ?? ""
    );

    const { query, language = "en" }: QueryRequest = await req.json();

    if (!query || query.trim().length === 0) {
      return new Response(
        JSON.stringify({ error: "Query cannot be empty" }),
        {
          status: 400,
          headers: { ...corsHeaders, "Content-Type": "application/json" },
        }
      );
    }

    const queryLower = query.toLowerCase().trim();
    const category = detectCategory(queryLower);

    const { data: cachedQuery } = await supabase
      .from("query_cache")
      .select("*")
      .eq("query_lower", queryLower)
      .eq("language", language)
      .maybeSingle();

    if (cachedQuery) {
      await supabase
        .from("query_cache")
        .update({
          hit_count: cachedQuery.hit_count + 1,
          updated_at: new Date().toISOString()
        })
        .eq("id", cachedQuery.id);

      return new Response(
        JSON.stringify({
          answer: cachedQuery.answer,
          source: "cache",
          category: cachedQuery.category,
        } as QueryResponse),
        {
          headers: { ...corsHeaders, "Content-Type": "application/json" },
        }
      );
    }

    const { data: knowledge } = await supabase
      .from("agricultural_knowledge")
      .select("*")
      .eq("language", language)
      .eq("category", category)
      .limit(5);

    const answer = generateContextualAnswer(query, category, knowledge || []);

    await supabase.from("query_cache").insert({
      query: query,
      query_lower: queryLower,
      language: language,
      answer: answer,
      category: category,
    });

    return new Response(
      JSON.stringify({
        answer: answer,
        source: "local",
        category: category,
      } as QueryResponse),
      {
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      }
    );
  } catch (error) {
    console.error("Error processing query:", error);

    return new Response(
      JSON.stringify({
        error: "Failed to process query",
        answer: "Sorry, I encountered an error processing your request. Please try again.",
        source: "error"
      }),
      {
        status: 500,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      }
    );
  }
});
