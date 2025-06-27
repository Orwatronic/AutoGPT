#!/usr/bin/env python3
"""
Property Intelligence RAG System
Vector-based retrieval for Gulf real estate investment knowledge
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import numpy as np
from dataclasses import dataclass

@dataclass
class PropertyDocument:
    property_id: str
    content: str
    metadata: Dict
    embedding: Optional[List[float]] = None

class PropertyRAGSystem:
    """RAG system for property investment intelligence"""
    
    def __init__(self):
        self.documents: List[PropertyDocument] = []
        self.property_embeddings = {}
        self.market_knowledge = self._load_market_knowledge()
        
    def _load_market_knowledge(self) -> Dict:
        """Load comprehensive market knowledge base"""
        return {
            'investment_strategies': {
                'beginner': {
                    'focus': 'Established markets with high liquidity',
                    'property_types': ['Apartments in Dubai Marina', 'Townhouses in established communities'],
                    'budget_allocation': 'Single property focus, 20% cash buffer',
                    'risk_level': 'Low to Medium'
                },
                'intermediate': {
                    'focus': 'Diversified portfolio across 2-3 markets',
                    'property_types': ['Mix of apartments and villas', 'Consider off-plan developments'],
                    'budget_allocation': '60% established, 40% growth markets',
                    'risk_level': 'Medium'
                },
                'advanced': {
                    'focus': 'Multi-market portfolio with currency diversification',
                    'property_types': ['Commercial properties', 'Luxury residential', 'Development projects'],
                    'budget_allocation': 'Strategic allocation based on market cycles',
                    'risk_level': 'Medium to High'
                }
            },
            'market_insights': {
                'Dubai': {
                    'best_for': 'International investors seeking liquidity',
                    'growth_drivers': ['Tourism recovery', 'Expo legacy', 'Golden visa program'],
                    'challenges': ['Market maturity', 'High competition'],
                    'recommended_areas': ['Business Bay', 'Dubai Hills', 'Mohammed Bin Rashid City']
                },
                'Riyadh': {
                    'best_for': 'Growth-focused investors with longer horizon',
                    'growth_drivers': ['Vision 2030', 'NEOM project', 'Economic diversification'],
                    'challenges': ['Market development', 'Regulatory changes'],
                    'recommended_areas': ['King Abdullah Financial District', 'Diplomatic Quarter', 'Al Olaya']
                },
                'Doha': {
                    'best_for': 'Stable returns with government backing',
                    'growth_drivers': ['World Cup legacy', 'LNG revenues', 'Infrastructure development'],
                    'challenges': ['Limited supply', 'Expat dependency'],
                    'recommended_areas': ['The Pearl', 'Lusail', 'West Bay']
                }
            }
        }
    
    def ingest_property_data(self, properties: List[Dict]) -> None:
        """Convert property data into searchable documents"""
        print(f"🔄 Ingesting {len(properties)} properties into RAG system...")
        
        for prop in properties:
            # Create comprehensive property description
            content = self._create_property_description(prop)
            
            doc = PropertyDocument(
                property_id=prop.get('property_id', 'unknown'),
                content=content,
                metadata={
                    'city': prop.get('location_city', ''),
                    'area': prop.get('location_area', ''),
                    'price': prop.get('price', 0),
                    'currency': prop.get('currency', ''),
                    'property_type': prop.get('property_type', ''),
                    'bedrooms': prop.get('bedrooms', 0),
                    'size_sqft': prop.get('size_sqft', 0),
                    'price_per_sqft': prop.get('price_per_sqft', 0)
                }
            )
            
            self.documents.append(doc)
        
        print(f"✅ RAG system loaded with {len(self.documents)} property documents")
    
    def _create_property_description(self, prop: Dict) -> str:
        """Create rich text description for RAG retrieval"""
        description = f"""
Property: {prop.get('title', 'Property listing')}
Location: {prop.get('location_area', '')}, {prop.get('location_city', '')}
Price: {prop.get('price', 0):,} {prop.get('currency', '')}
Type: {prop.get('property_type', '')} with {prop.get('bedrooms', 0)} bedrooms
Size: {prop.get('size_sqft', 0):,} sqft
Price per sqft: {prop.get('price_per_sqft', 0):.2f}
        """.strip()
        
        return description
    
    def search_properties(self, query: str, filters: Dict = None, top_k: int = 5) -> List[Dict]:
        """Search properties using semantic similarity"""
        query_lower = query.lower()
        relevant_docs = []
        
        for doc in self.documents:
            relevance_score = 0
            
            # Keyword matching
            if any(word in doc.content.lower() for word in query_lower.split()):
                relevance_score += 1
            
            # Filter matching
            if filters:
                if filters.get('city') and filters['city'].lower() in doc.metadata.get('city', '').lower():
                    relevance_score += 2
                if filters.get('max_price') and doc.metadata.get('price', 0) <= filters['max_price']:
                    relevance_score += 1
            
            if relevance_score > 0:
                relevant_docs.append({
                    'document': doc,
                    'relevance_score': relevance_score
                })
        
        # Sort by relevance and return top results
        relevant_docs.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return [
            {
                'property_id': doc['document'].property_id,
                'content': doc['document'].content,
                'metadata': doc['document'].metadata,
                'relevance_score': doc['relevance_score']
            }
            for doc in relevant_docs[:top_k]
        ]

def main():
    """Test the RAG system"""
    print("🧠 INITIALIZING PROPERTY RAG SYSTEM...")
    
    rag_system = PropertyRAGSystem()
    print("✅ RAG SYSTEM OPERATIONAL")
    return rag_system

if __name__ == "__main__":
    rag_system = main()
