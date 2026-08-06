from __future__ import annotations


class ExecutionValidator:
    """
    Validates whether an execution plan is eligible.
    """

    def validate(
        self,
        *,
        asset_exists: bool,
        workflow_exists: bool,
        automation_enabled: bool,
        permission_granted: bool,
    ) -> bool:

        return all(
            (
                asset_exists,
                workflow_exists,
                automation_enabled,
                permission_granted,
            )
        )