import json
from mcp_server.api_client import get_client

def register_user_tools(mcp):
    @mcp.tool()
    async def list_users() -> str:
        """List all users.
        
        Use this tool to view all users in the system.
        
        Returns:
            JSON string containing a list of users.
        """
        client = get_client()
        try:
            users = await client.get_users()
            return json.dumps(users, indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)})

    @mcp.tool()
    async def get_user(user_id: str) -> str:
        """Get details for a specific user.
        
        Args:
            user_id: The UUID of the user.
            
        Returns:
            JSON string with user details.
        """
        client = get_client()
        try:
            user = await client.get_user(user_id)
            return json.dumps(user, indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)})

    @mcp.tool()
    async def create_user(name: str, email: str, password: str, system_role_id: str = None) -> str:
        """Create a new user in the PM Tool from the external CRM.
        Password is required.
        """
        client = get_client()
        data = {"name": name, "email": email, "password": password}
        if system_role_id:
            data["system_role_id"] = system_role_id
        try:
            user = await client.create_user(data)
            return json.dumps(user, indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)})

    @mcp.tool()
    async def update_user(user_id: str, name: str = None, email: str = None, system_role_id: str = None) -> str:
        """Update an existing user in the PM Tool."""
        client = get_client()
        data = {}
        if name:
            data["name"] = name
        if email:
            data["email"] = email
        if system_role_id:
            data["system_role_id"] = system_role_id
            
        try:
            user = await client.update_user(user_id, data)
            return json.dumps(user, indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)})

    @mcp.tool()
    async def delete_user(user_id: str) -> str:
        """Delete (soft-delete) a user from the PM Tool."""
        client = get_client()
        try:
            result = await client.delete_user(user_id)
            return json.dumps(result, indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)})

    @mcp.tool()
    async def get_user_by_email(email: str) -> str:
        """Look up a PM Tool user by their email address."""
        client = get_client()
        try:
            user = await client.get_user_by_email(email)
            return json.dumps(user, indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)})
