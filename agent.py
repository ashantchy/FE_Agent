import json
from typing import List, Dict

from llama_index.llms.openai import OpenAI
from llama_index.core.llms import ChatMessage
from llama_index.core.tools import BaseTool, FunctionTool

import nest_asyncio
nest_asyncio.apply()

from pydantic import BaseModel
class ValidationResponse(BaseModel):
    valid: bool
    message: str

# Category hierarchy
CATEGORY_HIERARCHY: Dict[str, Dict[str, List[str]]] = {
    # Electronics Category
    "Electronics": {
        "Mobile": ["Smartphone", "Feature Phone", "Flip Phone"],
        "Laptop": ["Gaming", "Ultrabook", "Business", "Chromebook"],
        "TV": ["LED", "OLED", "Smart TV", "4K TV"],
        "Headphones": ["Over-Ear", "In-Ear", "Noise Cancelling", "Bluetooth"],
        "Camera": ["DSLR", "Mirrorless", "Point & Shoot"],
    },
    
    # Furniture Category
    "Furniture": {
        "Chair": ["Office", "Gaming", "Recliner", "Dining"],
        "Table": ["Dining", "Coffee", "Side", "Office Desk", "Console"],
        "Sofa": ["Leather", "Fabric", "Reclining", "Sectional"],
        "Bed": ["King", "Queen", "Twin", "Bunk"],
        "Storage": ["Cabinet", "Shelf", "Bookcase", "Wardrobe"],
    },

    # Clothing Category
    "Clothing": {
        "Men": ["T-Shirts", "Jeans", "Jackets", "Suits", "Shorts"],
        "Women": ["Dresses", "Blouses", "Tops", "Skirts", "Sweaters"],
        "Kids": ["Shirts", "Pants", "Jackets", "Dresses", "Hats"],
        "Footwear": ["Sneakers", "Boots", "Flip Flops", "Loafers", "Heels"],
    },

    # Kitchenware Category
    "Kitchenware": {
        "Cookware": ["Pots", "Pans", "Pressure Cookers", "Griddles", "Baking Sheets"],
        "Appliances": ["Microwave", "Blender", "Coffee Maker", "Toaster", "Grill"],
        "Utensils": ["Spoons", "Forks", "Knives", "Ladles", "Spatulas"],
        "Storage": ["Jars", "Containers", "Jugs", "Baskets", "Trays"],
        "Cutlery": ["Knives", "Forks", "Spoons", "Chopsticks", "Steak Knives"],
    },

    # Sports Category
    "Sports": {
        "Football": ["Soccer Ball", "Football Shoes", "Goalkeeper Gloves", "Jerseys"],
        "Basketball": ["Basketball", "Basketball Shoes", "Jerseys", "Hoops"],
        "Tennis": ["Rackets", "Tennis Balls", "Shoes", "Tennis Bags"],
        "Cycling": ["Bikes", "Helmets", "Gloves", "Knee Pads", "Lights"],
        "Gym Equipment": ["Dumbbells", "Resistance Bands", "Yoga Mats", "Treadmills"],
    },

    # Books Category
    "Books": {
        "Fiction": ["Thriller", "Romance", "Fantasy", "Mystery", "Adventure"],
        "Non-Fiction": ["Biography", "Self-Help", "Science", "History", "Politics"],
        "Children": ["Picture Books", "Early Readers", "Chapter Books", "Young Adult"],
        "Textbooks": ["Math", "Science", "History", "Literature", "Language Arts"],
        "Comics": ["Manga", "Graphic Novels", "Superhero", "Indie Comics"],
    },

    # Home Improvement Category
    "Home Improvement": {
        "Tools": ["Drills", "Hammers", "Wrenches", "Screwdrivers", "Plumbing Tools"],
        "Paint": ["Wall Paint", "Spray Paint", "Wood Stain", "Brushes", "Rollers"],
        "Gardening": ["Shovels", "Rakes", "Pots", "Seeds", "Fertilizers"],
        "Lighting": ["Ceiling Lights", "LED Bulbs", "Outdoor Lighting", "Floor Lamps"],
        "Plumbing": ["Pipes", "Faucets", "Showers", "Toilets", "Bathtubs"],
    },

    # Beauty & Personal Care Category
    "Beauty & Personal Care": {
        "Skincare": ["Moisturizers", "Face Masks", "Sunscreen", "Serums", "Toners"],
        "Haircare": ["Shampoos", "Conditioners", "Hair Oil", "Hair Masks", "Styling Tools"],
        "Makeup": ["Foundation", "Mascara", "Lipsticks", "Eyeliners", "Blush"],
        "Fragrance": ["Perfume", "Deodorant", "Body Spray", "Aftershave"],
        "Grooming": ["Razors", "Shaving Cream", "Beard Oil", "Trimmers", "Combs"],
    },

    # Toys & Games Category
    "Toys & Games": {
        "Action Figures": ["Superheroes", "Monsters", "Anime", "Video Game Characters"],
        "Puzzles": ["Jigsaw", "3D Puzzles", "Rubik's Cube", "Logic Puzzles"],
        "Board Games": ["Chess", "Monopoly", "Scrabble", "Clue", "Settlers of Catan"],
        "Educational Toys": ["STEM Kits", "Building Blocks", "Learning Apps", "Reading Toys"],
        "Outdoor Toys": ["Bicycles", "Skateboards", "Jump Ropes", "Frisbees"],
    },

    # Automotive Category
    "Automotive": {
        "Car Accessories": ["Seat Covers", "Floor Mats", "Steering Wheel Covers", "Car Cushions"],
        "Car Care": ["Car Wax", "Cleaning Cloths", "Polishes", "Tire Cleaner"],
        "Tools & Equipment": ["Car Jacks", "Battery Chargers", "Car Lifts", "Tool Kits"],
        "Parts": ["Brakes", "Tires", "Air Filters", "Batteries", "Lights"],
        "Electronics": ["Car GPS", "Dash Cams", "Car Speakers", "Stereo Systems"],
    },

    # Music Category
    "Music": {
        "Instruments": ["Guitar", "Piano", "Drums", "Violin", "Saxophone"],
        "Accessories": ["Picks", "Stands", "Tuners", "Cables", "Pedals"],
        "Headphones": ["Studio Headphones", "Bluetooth Headphones", "Noise-Cancelling"],
        "Vinyl": ["Rock", "Pop", "Jazz", "Classical", "Indie"],
        "Sheet Music": ["Piano", "Guitar", "Violin", "Saxophone", "Percussion"],
    },
    # Music Category
    "Muic": {
        "Instruments": ["Guitar", "Piano", "Drums", "Violin", "Saxophone"],
        "Accessories": ["Picks", "Stands", "Tuners", "Cables", "Pedals"],
        "Headphones": ["Studio Headphones", "Bluetooth Headphones", "Noise-Cancelling"],
        "Vinyl": ["Rock", "Pop", "Jazz", "Classical", "Indie"],
        "Sheet Music": ["Piano", "Guitar", "Violin", "Saxophone", "Percussion"],
    },
    # Music Category
    "usic": {
        "Instruments": ["Guitar", "Piano", "Drums", "Violin", "Saxophone"],
        "Accessories": ["Picks", "Stands", "Tuners", "Cables", "Pedals"],
        "Headphones": ["Studio Headphones", "Bluetooth Headphones", "Noise-Cancelling"],
        "Vinyl": ["Rock", "Pop", "Jazz", "Classical", "Indie"],
        "Sheet Music": ["Piano", "Guitar", "Violin", "Saxophone", "Percussion"],
    }
    
}


# Function to validate categories
def validate_category(category: str = None) -> dict:
    """
    Validates if the provided category exists in the CATEGORY_HIERARCHY. If no category is provided,
    returns a list of all valid categories.

    Args:
        category (str, optional): The category name to be validated.

    Returns:
        dict: A dictionary indicating whether the category is valid or not, and a list of valid categories if invalid.
              If no category is provided, returns the list of valid categories.
    """
    if category:
        category = category.strip().title()  # Normalize input
        if category in CATEGORY_HIERARCHY:
            return {"valid": True, "message": f"Yes, '{category}' is a valid category."}
        
        return {
            "valid": False,
            "message": f"No, '{category}' is invalid category.",
            "valid_categories": list(CATEGORY_HIERARCHY.keys())
        }
    else:
        return {
            "valid": True,
            "message": "Here are the valid categories:",
            "valid_categories": list(CATEGORY_HIERARCHY.keys())
        }

category_tool = FunctionTool.from_defaults(fn=validate_category)
"""
Tool for validating categories. It checks if a given category exists in the predefined CATEGORY_HIERARCHY.
If no category is provided, returns a list of all valid categories.
"""

# Function to validate types
def validate_type(category: str, type_name: str = None) -> dict:
    """
    Validates if the provided type name exists under a given category in CATEGORY_HIERARCHY. If no type is provided,
    returns a list of valid types under the given category.

    Args:
        category (str): The category name under which to validate the type.
        type_name (str, optional): The type name to be validated within the category.

    Returns:
        dict: A dictionary indicating whether the type is valid under the given category, and a list of valid types if invalid.
              If no type is provided, returns the list of valid types for the category.
    """
    category = category.strip().title()
    
    if category not in CATEGORY_HIERARCHY:
        return {
            "valid": False,
            "message": f"'{category}' is a invalid valid category.",
            "valid_categories": list(CATEGORY_HIERARCHY.keys())
        }

    if type_name:
        type_name = type_name.strip().title()
        valid_types = list(CATEGORY_HIERARCHY[category].keys())
        if type_name in valid_types:
            return {"valid": True, "message": f"Yes, '{type_name}' is a valid type under '{category}'."}
        
        return {
            "valid": False,
            "message": f"No, '{type_name}' is invalid type under '{category}'.",
            "valid_types": valid_types
        }
    
    # If no type is provided, return all valid types for the category
    return {
        "valid": True,
        "message": f"Here are the valid types for '{category}':",
        "valid_types": list(CATEGORY_HIERARCHY[category].keys())
    }

type_tool = FunctionTool.from_defaults(fn=validate_type)
"""
Tool for validating types. It checks if a given type exists under a specific category in the CATEGORY_HIERARCHY.
If no type is provided, returns a list of valid types for the specified category.
"""

# Function to validate sub-types
def validate_sub_type(type_name: str, sub_type: str = None, category: str = None) -> dict:
    """
    Validates if the provided sub-type exists under a given type and category (if category is provided) in CATEGORY_HIERARCHY. 
    If no category is provided, it validates based on type and sub-type only.
    
    Args:
        category (str, optional): The category name under which to validate the sub-type.
        type_name (str): The type name under which to validate the sub-type.
        sub_type (str, optional): The sub-type name to be validated within the specified type and category if given.

    Returns:
        dict: A dictionary indicating whether the sub-type is valid under the given type and category, 
              and a list of valid sub-types if invalid.
              If no sub-type is provided, returns the list of valid sub-types for the type and category.
    """
    type_name = type_name.strip().title()
    
    # Handle case where category is provided
    if category:
        category = category.strip().title()
        if category not in CATEGORY_HIERARCHY:
            return {
                "valid": False,
                "message": f"'{category}' is not a valid category.",
                "valid_categories": list(CATEGORY_HIERARCHY.keys())
            }

        if type_name not in CATEGORY_HIERARCHY[category]:
            return {
                "valid": False,
                "message": f"'{type_name}' is not a valid type under '{category}'.",
                "valid_types": list(CATEGORY_HIERARCHY[category].keys())
            }
        
        # Validate sub-type if provided
        if sub_type:
            sub_type = sub_type.strip().title()
            valid_sub_types = CATEGORY_HIERARCHY[category][type_name]
            if sub_type in valid_sub_types:
                return {"valid": True, "message": f"Yes, '{sub_type}' is a valid sub-type under '{type_name}' in category '{category}'."}
            return {
                "valid": False,
                "message": f"No, '{sub_type}' is an invalid sub-type under '{type_name}'.",
                "valid_sub_types": valid_sub_types
            }

        # If no sub-type is provided, return all valid sub-types for the type under this category
        return {
            "valid": True,
            "message": f"Here are the valid sub-types for '{type_name}' under category '{category}':",
            "valid_sub_types": CATEGORY_HIERARCHY[category][type_name]
        }

    # If category is not provided, check against all categories
    else:
        valid_categories_for_type = [cat for cat in CATEGORY_HIERARCHY if type_name in CATEGORY_HIERARCHY[cat]]
        if not valid_categories_for_type:
            return {
                "valid": False,
                "message": f"'{type_name}' is not a valid type in any category.",
                "valid_categories_for_type": valid_categories_for_type
            }
        
        # Validate sub-type if provided under all valid categories
        if sub_type:
            sub_type = sub_type.strip().title()
            for cat in valid_categories_for_type:
                if type_name in CATEGORY_HIERARCHY[cat]:
                    valid_sub_types = CATEGORY_HIERARCHY[cat][type_name]
                    if sub_type in valid_sub_types:
                        return {"valid": True, "message": f"Yes, '{sub_type}' is a valid sub-type under '{type_name}' in category '{cat}'."}
                    else:
                        return {
                            "valid": False,
                            "message": f"No, '{sub_type}' is an invalid sub-type under '{type_name}' in category '{cat}'.",
                            "valid_sub_types": valid_sub_types
                        }
            
        # If no sub-type is provided, return all valid sub-types for the type across all categories
        return {
            "valid": True,
            "message": f"Here are the valid sub-types for '{type_name}' across all categories:",
            "valid_sub_types": [sub_type for cat in valid_categories_for_type for sub_type in CATEGORY_HIERARCHY[cat].get(type_name, [])]
        }



sub_type_tool = FunctionTool.from_defaults(fn=validate_sub_type)
"""
Tool for validating sub-types. It checks if a given sub-type exists under a specific type and category in the CATEGORY_HIERARCHY.
If no sub-type is provided, returns a list of valid sub-types for the specified type and category.
"""

# Tools list to integrate with Ollama

tools = [category_tool, type_tool, sub_type_tool]
"""
A list of tools used for validating categories, types, and sub-types. These tools interact with the LLM to perform validation tasks.
"""

import os
from llama_index.llms.ollama import Ollama

# Initialize Ollama LLM
llm = Ollama(model="llama3:latest", base_url="http://192.168.20.106:11434", temperature=0)

from llama_index.core.agent import ReActAgent

# Ensure a single iteration to avoid redundant queries
agent = ReActAgent.from_tools(tools, llm=llm, verbose=True, max_iterations=20)




# -----------------------------
# Dataclass & Conversion Function for Entity Extraction
# -----------------------------
from typing import Optional
import re

def extract_json_from_text(text: str) -> Optional[str]:
    """
    Attempts to extract a JSON string from text.
    First, looks for a JSON code block wrapped in triple backticks.
    If not found, searches for a generic JSON object.
    """
    # Try to find a JSON code block (with or without "json" after backticks)
    code_block_regex = r"```(?:json)?\s*([\s\S]*?)\s*```"
    match = re.search(code_block_regex, text)
    if match:
        candidate = match.group(1).strip()
        return candidate

    # Fallback: try to locate any JSON object
    json_regex = r"(\{[\s\S]*\})"
    match = re.search(json_regex, text)
    if match:
        candidate = match.group(1).strip()
        return candidate

    return None

def convert_prompt_to_validation_response(message: str, llm: Ollama) -> ValidationResponse:
    """
    Uses the LLM to extract validation information from an arbitrary prompt.
    Returns a ValidationResponse instance populated with the extracted information.
    """
    extraction_prompt = (
    f"Analyze the following text exactly as it is: '{message}'. "
    "Determine whether the text indicates that a category validation is successful or unsuccessful, following these strict rules:\n"
    "1. If any part of the text explicitly states that a category, type, or sub-type is invalid (e.g., 'No, \"meta\" is not a subtype of Electronics or any other category.' or 'No, a cabinet is not a type of sofa.'), then the overall validation must be false.\n"
    "2. If the text **only** lists valid categories, types, or sub-types (e.g., 'The valid categories are Electronics, Furniture. Under Electronics, the valid types are Mobile, Laptop, TV, etc.'), but does not explicitly confirm validation, then the overall validation must be false.\n"
    "3. If the text contains both valid and invalid statements, the presence of any explicit invalid statement forces the overall validation to be false.\n"
    "4. The validation is true **only** if the text explicitly confirms that a category validation check was successful (e.g., 'Yes, Electronics is a valid category.') and no invalid statement is present.\n"
    "5. The overall validation should be true only if the text exclusively indicates that a category is valid, without any indication of an invalid category or type.\n"
    "Return ONLY a JSON object with exactly two keys:\n"
    "  - \"valid\": a boolean that is true **only** if the text explicitly confirms a successful validation, otherwise false.\n"
    "  - \"message\": the entire original input text exactly as provided, without any modification.\n"
    "Your response must be a valid JSON object with no extra text and using double quotes for all keys and string values."
)



    try:
        response_text = llm.complete(extraction_prompt).text
        json_str = extract_json_from_text(response_text)
        if not json_str:
            print("Could not extract JSON from LLM response.")
            return ValidationResponse(
                valid=False,
                message="Could not extract JSON from LLM response",
            )
        
        try:
            data = json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            print("LLM output is not valid JSON. Raw output:")
            print(response_text)
            return ValidationResponse(
                valid=False,
                message="Invalid JSON output",
            )
        
        parsed_data = {
            "valid": data.get("valid", False),
            # Force the message to be the entire original input text.
            "message": str(message),
        }
        
        response_obj = ValidationResponse(**parsed_data)
        return response_obj
        
    except Exception as e:
        print(f"Unexpected error during LLM call: {e}")
        return ValidationResponse(
            valid=False,
            message=f"Error: {e}",
        )





def answer_chat(prompt:str):
    response = agent.query(prompt)
    validation_response = convert_prompt_to_validation_response(response, llm)
    return validation_response


