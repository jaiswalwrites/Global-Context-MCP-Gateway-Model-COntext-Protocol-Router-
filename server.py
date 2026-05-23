import uvicorn
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("MCP-Gateway")

app = FastAPI(title="Global Context MCP Gateway", version="1.0.0")

class QueryRequest(BaseModel):
    query: str
    user_context: Optional[Dict] = None

class MCPRouteResponse(BaseModel):
    target_node: str
    action: str
    confidence: float
    context_tokens_optimized: int
    payload: Dict

INTENT_KEYWORDS = {
    "vector": ("vector_mcp_node", "query_semantic_index", 0.95),
    "database": ("vector_mcp_node", "query_semantic_index", 0.92),
    "sql": ("sql_analytics_node", "execute_bi_query", 0.96),
    "web": ("web_crawler_node", "fetch_external_results", 0.89),
    "search": ("web_crawler_node", "fetch_external_results", 0.87),
    "cost": ("finops_cost_node", "retrieve_billing_data", 0.94),
    "spend": ("finops_cost_node", "retrieve_billing_data", 0.91)
}

@app.post("/mcp/route", response_model=MCPRouteResponse)
async def route_query(request: QueryRequest):
    logger.info(f"Incoming query request: '{request.query}'")
    query_lower = request.query.lower()
    
    target_node = "general_inference_node"
    action = "direct_llm_completion"
    confidence = 0.70
    
    for key, (node, act, conf) in INTENT_KEYWORDS.items():
        if key in query_lower:
            target_node = node
            action = act
            confidence = conf
            break
            
    optimized_tokens = len(request.query) * 12
    return MCPRouteResponse(
        target_node=target_node,
        action=action,
        confidence=confidence,
        context_tokens_optimized=optimized_tokens,
        payload={"original_query": request.query, "metadata": request.user_context}
    )

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Refactored update: stage 4 checkpoint - 2026-05-23
