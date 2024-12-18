#!/bin/bash

# Define the base URL for the Flask API
BASE_URL="http://localhost:5000/api"

# Flag to control whether to echo JSON output
ECHO_JSON=false

# Parse command-line arguments
while [ "$#" -gt 0 ]; do
  case $1 in
    --echo-json) ECHO_JSON=true ;;
    *) echo "Unknown parameter passed: $1"; exit 1 ;;
  esac
  shift
done

# Function to check the health of the service
check_health() {
  echo "Checking health status..."
  curl -s -X GET "$BASE_URL/health" | grep -q '"status": "healthy"'
  if [ $? -eq 0 ]; then
    echo "Service is healthy."
  else
    echo "Health check failed."
    exit 1
  fi
}

# Function to check the database connection
check_db() {
  echo "Checking database connection..."
  curl -s -X GET "$BASE_URL/db-check" | grep -q '"database_status": "healthy"'
  if [ $? -eq 0 ]; then
    echo "Database connection is healthy."
  else
    echo "Database check failed."
    exit 1
  fi
}

create_meal() {
  meal=$1
  cuisine=$2
  price=$3
  difficulty=$4

  echo "Adding meal ($meal, $cuisine, $price, $difficulty) to the combatant list..."
  curl -s -X POST "$BASE_URL/create-meal" -H "Content-Type: application/json" \
    -d "{\"meal\":\"$meal\", \"cuisine\":\"$cuisine\", \"price\":\"$price\", \"difficulty\":\"$difficulty\"}" | grep -q '"status": "success"'

  if [ $? -eq 0 ]; then
    echo "meal added successfully."
  else
    echo "Failed to add meal."
    exit 1
  fi
}

delete_meal() {
  meal_id=$1

  echo "Deleting meal by ID ($meal_id)..."
  response=$(curl -s -X DELETE "$BASE_URL/delete-meal/$meal_id")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "meal deleted successfully by ID ($meal_id)."
  else
    echo "Failed to delete meal by ID ($meal_id)."
    exit 1
  fi
}

get_combatants() {
  echo "Getting all meals in the combatants list..."
  response=$(curl -s -X GET "$BASE_URL/get-combatants")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "All meals retrieved successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Meals JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to get meals."
    exit 1
  fi
}

get_meal_by_id() {
  meal_id=$1

  echo "Getting meal by ID ($meal_id)..."
  response=$(curl -s -X GET "$BASE_URL/get-meal-by-id/$meal_id")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "meal retrieved successfully by ID ($meal_id)."
    if [ "$ECHO_JSON" = true ]; then
      echo "meal JSON (ID $meal_id):"
      echo "$response" | jq .
    fi
  else
    echo "Failed to get meal by ID ($meal_id)."
    exit 1
  fi
}

prep_combatant() {
  meal=$1
  cuisine=$2
  price=$3
  difficult=$4

  echo "Adding meal to combatants list: $meal - $cuisine ($price, $difficult)..."
  response=$(curl -s -X POST "$BASE_URL/prep-combatant" \
    -H "Content-Type: application/json" \
    -d "{\"meal\":\"$meal\", \"cuisine\":\"$cuisine\", \"price\":$price, \"difficult\":\"$difficult\"}")

  if echo "$response" | grep -q '"status": "success"'; then
    echo "meal added to combatants list successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "meal JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to add meal to combatants list."
    exit 1
  fi
}

delete_meal() {
  id=$1

  echo "Removing meal by id: $id..."
  response=$(curl -s -X DELETE "$BASE_URL/delete-meal/$id")

  if echo "$response" | grep -q '"status":'; then
    echo "meal removed from combatant list by id ($id) successfully."
  else
    echo "Failed to remove meal from combatant list by id."
    exit 1
  fi
}

clear_combatants() {
  echo "Clearing combatants list..."
  response=$(curl -s -X POST "$BASE_URL/clear-combatants")

  if echo "$response" | grep -q '"status": "success"'; then
    echo "Combatants list cleared successfully."
  else
    echo "Failed to clear combatants list."
    exit 1
  fi
}

battle() {
  echo "Battling current combatants..."
  curl -s -X GET "$BASE_URL/battle" | grep -q '"status": "success"'

  if [ $? -eq 0 ]; then
    echo "combatants battled successfully."
  else
    echo "Failed to battle combatants."
    exit 1
  fi
}

get_leaderboard() {
  sort_by=$1
  echo "Getting leaderboard sorted by $sort_by..."
  response=$(curl -s -X GET "$BASE_URL/leaderboard?sort_by=$sort_by")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Leaderboard retrieved successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Leaderboard JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to get leaderboard."
    exit 1
  fi
}

check_health
check_db

create_meal "Spaghetti Bolognese" "Pasta" 30 "HIGH"
create_meal "Chicken Salad" "Salad" 15 "MED"
create_meal "Grilled Cheese Sandwich" "Sandwich" 10 "MED"
create_meal "Beef Stew" "Stew" 60 "HIGH"
create_meal "Veggie Stir-fry" "Stir-fry" 25 "LOW"

delete_meal 1

get_meal_by_id 2

prep_combatant "Chicken Salad" "Salad" 15 "MED"
prep_combatant "Beef Stew" "Stew" 60 "HIGH"
battle

clear_combatants

prep_combatant "Beef Stew" "Stew" 60 "HIGH"
prep_combatant "Veggie Stir-fry" "Stir-fry" 25 "LOW"
battle
get_combatants

delete_meal 3

get_leaderboard "wins"

echo "All tests passed successfully!"