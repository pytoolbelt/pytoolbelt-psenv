import logging
from psenv.core.diff import ParameterDiff
from psenv.core.context import Context


class Synchronizer:
    def __init__(self, dry_run: bool) -> None:
        self.dry_run = dry_run
        self.logger = logging.getLogger("psenv.synchronizer")

    def sync(self, ctx: Context, param_diff: ParameterDiff, mode: str, overwrite: bool):
        if self.dry_run:
            if mode == "sync":
                self._log_dry_run_to_add(param_diff)
                self._log_dry_run_to_update(param_diff)
                self._log_dry_run_to_remove(param_diff)

            elif mode == "add" and not overwrite:
                self._log_dry_run_to_add(param_diff)

            elif mode == "update" and overwrite:
                self._log_dry_run_to_update(param_diff)
                self._log_dry_run_to_update(param_diff)
            return

        if mode == "sync":
            self.logger.info("Syncing parameters with the parameter store.")
            ctx.ps_client.put_parameters(param_diff.to_add)
            ctx.ps_client.put_parameters(param_diff.to_update, overwrite=True)
            self.logger.info("Removing parameters that are not in the local environment file.")
            ctx.ps_client.delete_parameters(param_diff.to_remove)

        elif mode == "add" and not overwrite:
            self.logger.info("Adding new parameters to the parameter store.")
            ctx.ps_client.put_parameters(param_diff.to_add)

        elif mode == "add" and overwrite:
            self.logger.info("Overwriting existing parameters in the parameter store.")
            ctx.ps_client.put_parameters(param_diff.to_add)
            ctx.ps_client.put_parameters(param_diff.to_update, overwrite=True)

    def _log_dry_run_to_add(self, param_diff: ParameterDiff) -> None:
        for key in param_diff.to_add:
            self.logger.info("[DRY RUN] Would add parameters: %s", key)

    def _log_dry_run_to_update(self, param_diff: ParameterDiff) -> None:
        for key in param_diff.to_update:
            self.logger.info("[DRY RUN] Would update parameters: %s", key)

    def _log_dry_run_to_remove(self, param_diff: ParameterDiff) -> None:
        for key in param_diff.to_remove:
            self.logger.info("[DRY RUN] Would remove parameters: %s", key)
