import httpx
from typing import Optional, Dict, Any, List
from mcp_server.config import mcp_settings

class PMToolAPIClient:
    def __init__(self, token: str):
        self.base_url = mcp_settings.PMTOOL_API_BASE_URL.rstrip('/')
        self.headers = {"Authorization": f"Bearer {token}"}

    async def _get(self, path: str) -> Any:
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.headers, timeout=60.0) as client:
            response = await client.get(path)
            response.raise_for_status()
            return response.json()

    async def _post(self, path: str, json_data: Dict[str, Any]) -> Any:
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.headers, timeout=60.0) as client:
            response = await client.post(path, json=json_data)
            response.raise_for_status()
            return response.json()

    async def _put(self, path: str, json_data: Dict[str, Any]) -> Any:
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.headers, timeout=60.0) as client:
            response = await client.put(path, json=json_data)
            response.raise_for_status()
            return response.json()

    async def _patch(self, path: str, json_data: Dict[str, Any]) -> Any:
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.headers, timeout=60.0) as client:
            response = await client.patch(path, json=json_data)
            response.raise_for_status()
            return response.json()

    async def _delete(self, path: str) -> Any:
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.headers, timeout=60.0) as client:
            response = await client.delete(path)
            response.raise_for_status()
            # Handle 204 No Content
            if response.status_code == 204 or not response.content:
                return {"message": "Success"}
            return response.json()

    async def _external_get(self, path: str) -> Any:
        headers = {**self.headers, "X-API-Key": mcp_settings.PMTOOL_EXTERNAL_API_KEY}
        async with httpx.AsyncClient(base_url=self.base_url, headers=headers, timeout=60.0) as client:
            response = await client.get(path)
            response.raise_for_status()
            return response.json()

    async def _external_post(self, path: str, json_data: Dict[str, Any]) -> Any:
        headers = {**self.headers, "X-API-Key": mcp_settings.PMTOOL_EXTERNAL_API_KEY}
        async with httpx.AsyncClient(base_url=self.base_url, headers=headers, timeout=60.0) as client:
            response = await client.post(path, json=json_data)
            response.raise_for_status()
            return response.json()

    async def _external_patch(self, path: str, json_data: Dict[str, Any]) -> Any:
        headers = {**self.headers, "X-API-Key": mcp_settings.PMTOOL_EXTERNAL_API_KEY}
        async with httpx.AsyncClient(base_url=self.base_url, headers=headers, timeout=60.0) as client:
            response = await client.patch(path, json=json_data)
            response.raise_for_status()
            return response.json()

    async def _external_delete(self, path: str) -> Any:
        headers = {**self.headers, "X-API-Key": mcp_settings.PMTOOL_EXTERNAL_API_KEY}
        async with httpx.AsyncClient(base_url=self.base_url, headers=headers, timeout=60.0) as client:
            response = await client.delete(path)
            response.raise_for_status()
            if response.status_code == 204 or not response.content:
                return {"message": "Success"}
            return response.json()

    # --- Projects ---
    async def get_projects(self) -> List[Dict[str, Any]]:
        return await self._get("/projects/")

    async def get_project(self, project_id: str) -> Dict[str, Any]:
        return await self._get(f"/projects/{project_id}")

    async def create_project(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return await self._post("/projects/", data)

    async def update_project(self, project_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        return await self._patch(f"/projects/{project_id}", data)

    async def delete_project(self, project_id: str) -> Dict[str, Any]:
        return await self._delete(f"/projects/{project_id}")

    # --- Tasks ---
    async def get_tasks(self, project_id: Optional[str] = None) -> List[Dict[str, Any]]:
        if project_id:
            return await self._get(f"/tasks/project/{project_id}")
        return await self._get("/tasks/")

    async def get_task(self, task_id: str) -> Dict[str, Any]:
        return await self._get(f"/tasks/{task_id}")

    async def create_task(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return await self._post("/tasks/", data)

    async def update_task(self, task_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        return await self._patch(f"/tasks/{task_id}", data)

    async def delete_task(self, task_id: str) -> Dict[str, Any]:
        return await self._delete(f"/tasks/{task_id}")

    async def change_task_status(self, task_id: str, status_id: str) -> Dict[str, Any]:
        return await self._patch(f"/tasks/{task_id}", {"status_id": status_id})

    async def assign_task(self, task_id: str, assignee_id: str) -> Dict[str, Any]:
        return await self._patch(f"/tasks/{task_id}", {"assignee_id": assignee_id})

    # --- Sprints ---
    async def get_sprints(self, project_id: Optional[str] = None) -> List[Dict[str, Any]]:
        if project_id:
            return await self._get(f"/sprints/project/{project_id}")
        return await self._get("/sprints/")

    async def get_sprint(self, sprint_id: str) -> Dict[str, Any]:
        return await self._get(f"/sprints/{sprint_id}")

    async def create_sprint(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return await self._post("/sprints/", data)

    async def update_sprint(self, sprint_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        return await self._patch(f"/sprints/{sprint_id}", data)

    async def delete_sprint(self, sprint_id: str) -> Dict[str, Any]:
        return await self._delete(f"/sprints/{sprint_id}")

    # --- Teams ---
    async def get_teams(self) -> List[Dict[str, Any]]:
        return await self._get("/teams/")

    async def get_team(self, team_id: str) -> Dict[str, Any]:
        return await self._get(f"/teams/{team_id}")

    async def create_team(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return await self._post("/teams/", data)

    async def update_team(self, team_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        return await self._patch(f"/teams/{team_id}", data)

    async def add_team_member(self, team_id: str, user_id: str) -> Dict[str, Any]:
        return await self._post(f"/teams/{team_id}/members/{user_id}", {})

    async def remove_team_member(self, team_id: str, user_id: str) -> Dict[str, Any]:
        return await self._delete(f"/teams/{team_id}/members/{user_id}")

    # --- Users ---
    async def get_users(self) -> List[Dict[str, Any]]:
        return await self._get("/users/")

    async def get_user(self, user_id: str) -> Dict[str, Any]:
        return await self._get(f"/users/{user_id}")
        
    # --- Users (extended for external integration) ---
    async def create_user(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return await self._external_post("/external/users/", data)

    async def update_user(self, user_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        return await self._external_patch(f"/external/users/{user_id}", data)

    async def delete_user(self, user_id: str) -> Dict[str, Any]:
        return await self._external_delete(f"/external/users/{user_id}")

    async def get_user_by_email(self, email: str) -> Dict[str, Any]:
        return await self._external_get(f"/external/users/by-email/{email}")

    # --- Time Entries ---
    async def get_time_entries(self, task_id: Optional[str] = None) -> List[Dict[str, Any]]:
        if task_id:
            return await self._get(f"/time-entries/task/{task_id}")
        return await self._get("/time-entries/")

    async def start_timer(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return await self._post("/time-entries/start", data)

    async def stop_timer(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return await self._post("/time-entries/stop", data)

    async def log_time(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return await self._post("/time-entries/", data)

    # --- Analytics ---
    async def get_analytics_summary(self) -> Dict[str, Any]:
        return await self._get("/analytics/summary")

    async def get_user_workload(self, project_id: Optional[str] = None) -> List[Dict[str, Any]]:
        url = f"/analytics/user-workload?project_id={project_id}" if project_id else "/analytics/user-workload"
        return await self._get(url)

    # --- Clients ---
    async def get_clients(self) -> List[Dict[str, Any]]:
        return await self._get("/clients/")

    async def get_client(self, client_id: str) -> Dict[str, Any]:
        return await self._get(f"/clients/{client_id}")

    async def create_client(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return await self._post("/clients/", data)

    async def update_client(self, client_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        return await self._patch(f"/clients/{client_id}", data)

    async def delete_client(self, client_id: str) -> Dict[str, Any]:
        return await self._delete(f"/clients/{client_id}")

    # --- Portfolios ---
    async def get_portfolios(self) -> List[Dict[str, Any]]:
        return await self._get("/portfolios/")

    async def get_portfolio(self, portfolio_id: str) -> Dict[str, Any]:
        return await self._get(f"/portfolios/{portfolio_id}")

def get_client() -> PMToolAPIClient:
    # TODO: In a production environment with per-request OAuth 2.1 PKCE, 
    # this token should be extracted from the MCP Request Context instead of 
    # being hardcoded or loaded from the environment.
    token = mcp_settings.PMTOOL_API_TOKEN
    return PMToolAPIClient(token=token)
