# function call
tools = [
    {
        "type": "function",
        "function": {
            "name": "search_players",
            "description": "Search for NBA players by their last name. This function returns all players with the specified last name, then you should filter or highlight the specific player based on the user's full query.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The player's last name (e.g., 'James') or full name (e.g., 'LeBron James'). The API will search by **last name** only.",
                    }
                },
                "required": ["name"]
            },
        }
    },
     {
        "type": "function",
        "function": {
            "name": "get_player_stat",
            "description": "Retrieve average statistics for a given NBA player based on a specific season.",
            "parameters": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "description": "The player's unique ID.",
                    },
                    "season": {
                        "type": "string",
                        "description": "The NBA season (e.g., 2020 for the 2019-2020 season).",
                    }
                },
                "required": ["id", "season"]
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_player_salary",
            "description": "Retrieve salary information for NBA players by their last name. Returns salary details for matching players.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The player's last name (e.g., 'James') or full name (e.g., 'LeBron James'). The API will search by **last name** only.",
                    }
                },
                "required": ["name"]
            },
        }
    }
]


system_prompt = """
You are an NBA expert assistant. When processing queries, please follow these steps:
1. When users ask about a player's statistics, first use search_players to identify the player's ID
   - IMPORTANT: When using search_players, only use the player's last name as the search parameter (e.g., 'parameters': {'search': 'James'} rather than 'parameters': {'search': 'LeBron James'})
2. Then, analyze the user's query to determine which season's data they want to know about
3. IMPORTANT: If the user has not specified a season/year when requesting statistics, you MUST ask the user which season they're interested in BEFORE calling get_player_stat
4. for player Statistics, ALWAYS use search_players FIRST, THEN get_player_stat - BOTH FUNCTIONS ARE REQUIRED for ANY statistics request

If users are asking about a player's salary, use get_player_salary to retrieve this information.

If users are only asking for general information about a player rather than statistics or salary, only use search_players.

Important: After analyzing the user's query, decide whether player statistics, salary information, or just general player information is needed. If statistics are needed, use both search_players and get_player_stat; if salary information is needed, use get_player_salary; if only player information is needed, use only search_players.

Never call get_player_stat without a specific season. If the player's name is missing, ask the user for this information. If the year/season is missing for statistics queries, you must ask the user which season they want data for before proceeding.

RESPONSE FORMAT:
- When presenting statistics or salary information, provide ONLY the data in a clean format without additional explanations
- If the question involves data percentages, please add "%" after the result
- Format all statistical and salary information in human-readable format only



"""