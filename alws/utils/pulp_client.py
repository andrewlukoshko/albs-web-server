import asyncio
import urllib
from typing import Optional

import aiohttp


class PulpClient:

    def __init__(self, host: str, username: str, password: str):
        self._host = host
        self._username = username
        self._password = password
        self._auth = aiohttp.BasicAuth(self._username, self._password)

    async def create_build_rpm_repo(self, name: str) -> str:
        ENDPOINT = 'pulp/api/v3/repositories/rpm/rpm/'
        payload = {'name': name, 'autopublish': True}
        response = await self.make_post_request(ENDPOINT, data=payload)
        repo_href = response['pulp_href']
        await self.create_publication(repo_href)
        distro = await self.create_distro(name, repo_href)
        return distro, repo_href

    async def create_publication(self, repository: str):
        ENDPOINT = 'pulp/api/v3/publications/rpm/rpm/'
        payload = {'repository': repository}
        task = await self.make_post_request(ENDPOINT, data=payload)
        await self.wait_for_task(task['task'])

    async def create_rpm_package(
                self,
                package_name: str,
                artifact_href: str,
                repo: str
            ) -> str:
        ENDPOINT = 'pulp/api/v3/content/rpm/packages/'
        payload = {
            'relative_path': package_name,
            'artifact': artifact_href,
            'repository': repo
        }
        task = await self.make_post_request(ENDPOINT, data=payload)
        task_result = await self.wait_for_task(task['task'])
        return task_result['created_resources'][0]

    async def create_distro(self, name: str, repository: str) -> str:
        ENDPOINT = 'pulp/api/v3/distributions/rpm/rpm/'
        payload = {
            'repository': repository,
            'name': f'{name}-distro',
            'base_path': f'builds/{name}'
        }
        task = await self.make_post_request(ENDPOINT, data=payload)
        task_result = await self.wait_for_task(task['task'])
        distro = await self.get_distro(task_result['created_resources'][0])
        return distro['base_url']

    async def get_distro(self, distro_href: str):
        return await self.make_get_request(distro_href)

    async def wait_for_task(self, task_href: str):
        task = await self.make_get_request(task_href)
        while task['state'] not in ('failed', 'completed'):
            await asyncio.sleep(0.3)
            task = await self.make_get_request(task_href)
        return task

    async def make_get_request(self, endpoint: str):
        full_url = urllib.parse.urljoin(self._host, endpoint)
        async with aiohttp.ClientSession(auth=self._auth) as session:
            async with session.get(full_url) as response:
                response.raise_for_status()
                return await response.json()

    async def make_post_request(self, endpoint: str, data: Optional[dict]):
        full_url = urllib.parse.urljoin(self._host, endpoint)
        async with aiohttp.ClientSession(auth=self._auth) as session:
            async with session.post(full_url, json=data) as response:
                response.raise_for_status()
                return await response.json()
