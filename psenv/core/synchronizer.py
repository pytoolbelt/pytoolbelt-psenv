import logging
from psenv.core.diff import ParameterDiff
from psenv.core.context import Context
from psenv.error_handling.exceptions import PsenvCLIError

class Synchronizer:
    def __init__(self, ctx: Context, param_diff:ParameterDiff, mode: str, dry_run: bool) -> None:
        self.ctx = ctx
        self.param_diff = param_diff
        self.mode = mode
        self.dry_run = dry_run
        self.logger = logging.getLogger("psenv.synchronizer")

    def sync(self):
        if self.dry_run:
            self.execute_dry_run()
            return

    def execute_dry_run(self) -> None:
        if self.mode == "add":
            self._log_dry_run_to_add()

        elif self.mode == "update":
            self._log_dry_run_to_add()
            self._log_dry_run_to_update()

        elif self.mode == "sync":
            self._log_dry_run_to_add()
            self._log_dry_run_to_update()
            self._log_dry_run_to_remove()
        else:
            raise PsenvCLIError(f"Invalid mode: {self.mode}. Must be one of 'add', 'update', or 'sync'.")

    def _log_dry_run_to_add(self) -> None:
        for key in self.param_diff.to_add:
            self.logger.info("[DRY RUN] Would add parameters: %s", key)

    def _log_dry_run_to_update(self) -> None:
        for key in self.param_diff.to_update:
            self.logger.info("[DRY RUN] Would update parameters: %s", key)

    def _log_dry_run_to_remove(self) -> None:
        for key in self.param_diff.to_remove:
            self.logger.info("[DRY RUN] Would remove parameters: %s", key)

    @staticmethod
    def get_mode_from_cliargs(cliargs) -> str:
        return Synchronizer.get_mode_from_flags(cliargs.add, cliargs.update, cliargs.sync)

    @staticmethod
    def get_mode_from_flags(add: bool, update: bool, sync: bool) -> str:
        flags = [add, update, sync]
        if sum(flags) != 1:
            raise ValueError("Exactly one of --add, --update, or --sync must be set.")
        if add:
            return "add"
        if update:
            return "update"
        if sync:
            return "sync"
        raise PsenvCLIError("Invalid mode flags.")
