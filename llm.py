import json
from openai import OpenAI
from nba_apis import search_players, get_player_stat, get_player_salary
import streamlit as st
from prompt import system_prompt, tools




def ask_llm(user_query, model, key):
    client = OpenAI(api_key=key)
    MAX_TURNS = 20
    """Simple function to process NBA queries and return text responses"""
    try:
        



        # Initialize or get conversation history from session state
        if "conversation_history" not in st.session_state:
            st.session_state.conversation_history = [
                {"role": "system", "content": system_prompt}
            ]
        
        # Add new user query to conversation history
        st.session_state.conversation_history.append({"role": "user", "content": user_query})

        # Apply sliding window to conversation history
        if len(st.session_state.conversation_history) > MAX_TURNS * 2 + 1:  # +1 for system message
            messages = [st.session_state.conversation_history[0]] + st.session_state.conversation_history[-(MAX_TURNS * 2):]
        else:
            messages = st.session_state.conversation_history.copy()


        # Get response from model
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            #tool_choice={"type": "function", "function": {"name": "search_players"}}  # 强制使用search_players
        )

        # If no tool calls, return the direct response
        if not response.choices[0].message.tool_calls:
            return response.choices[0].message.content
        
       # Check if the model suggests a tool call
       
        st.session_state.conversation_history.append(response.choices[0].message)
        messages.append(response.choices[0].message)
            
    
        for tool in response.choices[0].message.tool_calls:
            if not hasattr(tool, 'function') or not hasattr(tool, 'id'):
                continue
            tool_name = tool.function.name
            try:
                tool_args = json.loads(tool.function.arguments)
            except json.JSONDecodeError:
                continue

            if tool_name == "search_players":
                player_name = tool_args["name"]
                player_data = search_players(player_name)
                
                # Add tool response to conversation
                if player_data is not None:
                    tool_response = {
                        "role": "tool",
                        "tool_call_id": tool.id,
                        "content": json.dumps(player_data)
                    }
                    messages.append(tool_response)
                    st.session_state.conversation_history.append(tool_response)

            if tool_name == "get_player_stat":
                print("Tool args:", tool_args)  # Add this to see what's actually in tool_args
                try:
                    if "player_id" in tool_args and "id" not in tool_args:
                        tool_args["id"] = tool_args["player_id"]

                    player_id = str(tool_args["id"]) 
                    print("Player ID:", player_id)
                    season = tool_args["season"]
                    stats_data = get_player_stat(player_id, season)
                except KeyError as e:
                    print(f"Missing key in tool_args: {e}")
                    continue  # Skip this tool call if key is missing
                
                # Add tool response to conversation
                if stats_data is not None:
                    tool_response = {
                        "role": "tool",
                        "tool_call_id": tool.id,
                        "content": json.dumps(stats_data)
                    }
                    messages.append(tool_response)
                    st.session_state.conversation_history.append(tool_response)
            
            if tool_name == "get_player_salary":
                    player_name = tool_args["name"]
                    player_data = get_player_salary(player_name)
                    
                    # Add tool response to conversation
                    if player_data is not None:
                        tool_response = {
                            "role": "tool",
                            "tool_call_id": tool.id,
                            "content": json.dumps(player_data)
                        }
                        messages.append(tool_response)
                        st.session_state.conversation_history.append(tool_response)


                # Get final response from the model after processing all tools
        final_response = client.chat.completions.create(
            model=model,
            messages=messages
        )

        return final_response.choices[0].message.content

    except Exception as e:
        print(f"Error: {e}")
        return f"Sorry, I encountered an error: {str(e)}"