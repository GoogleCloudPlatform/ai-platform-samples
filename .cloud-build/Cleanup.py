import abc
from google.cloud import aiplatform
from typing import Any, List


class ResourceCleanupManager(abc.ABC):
    @property
    @abc.abstractmethod
    def type_name(str) -> str:
        pass

    @abc.abstractmethod
    def list(self) -> Any:
        pass

    @abc.abstractmethod
    def resource_name(self, resource: Any) -> str:
        pass

    @abc.abstractmethod
    def delete(self, resource: Any):
        pass

    def is_deletable(self, resource: Any) -> bool:
        return not self.resource_name(resource).startswith("perm_")


class DatasetResourceCleanupManager(ResourceCleanupManager):
    type_name = "dataset"

    def list(self) -> Any:
        return aiplatform.datasets._Dataset.list()

    def resource_name(self, resource: Any) -> str:
        return resource.display_name

    def delete(self, resource):
        resource.delete()


class EndpointResourceCleanupManager(ResourceCleanupManager):
    type_name = "endpoint"

    def list(self) -> Any:
        return aiplatform.Endpoint.list()

    def resource_name(self, resource: Any) -> str:
        return resource.display_name

    def delete(self, resource):
        resource.delete(force=True)


class ModelResourceCleanupManager(ResourceCleanupManager):
    type_name = "model"

    def list(self) -> Any:
        return aiplatform.Model.list()

    def resource_name(self, resource: Any) -> str:
        return resource.display_name

    def delete(self, resource):
        resource.delete()


def cleanup_managers(managers: List[ResourceCleanupManager], is_dry_run: bool):
    for manager in managers:
        type_name = manager.type_name

        print(f"Fetching {type_name}'s...")
        resources = manager.list()
        print(f"Found {len(resources)} {type_name}'s")
        for resource in resources:
            if not manager.is_deletable(resource):
                continue

            if is_dry_run:
                resource_name = manager.resource_name(resource)
                print(f"Will delete '{type_name}': {resource_name}")
            else:
                manager.delete(resource)

        print("")


is_dry_run = True

if is_dry_run:
    print("Starting cleanup in dry run mode...")

managers = [
    DatasetResourceCleanupManager(),
    EndpointResourceCleanupManager(),
    ModelResourceCleanupManager(),
]

cleanup_managers(managers=managers, is_dry_run=is_dry_run)
