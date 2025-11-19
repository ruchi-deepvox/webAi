#!/bin/bash

echo "======================================"
echo "Testing Unified Voice Agent API"
echo "======================================"
echo ""

# Test 1: Health Check
echo "1. Health Check:"
curl -s http://localhost:8000/api/health | jq '.'
echo ""

# Test 2: Get Config
echo "2. API Configuration:"
curl -s http://localhost:8000/api/config | jq '.'
echo ""

# Test 3: Connect to Agent
echo "3. Connect to Agent (Main Test):"
curl -s -X POST http://localhost:8000/api/connect \
  -H "Content-Type: application/json" \
  -d '{"user_name": "Test User"}' | jq '.'
echo ""

# Test 4: List Rooms
echo "4. List Active Rooms:"
curl -s http://localhost:8000/api/rooms | jq '.'
echo ""

echo "======================================"
echo "All tests completed!"
echo "======================================"

