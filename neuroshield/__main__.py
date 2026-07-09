"""
NeuroShield CLI entry point.

Enables:
    python -m neuroshield run experiment.toml
    python -m neuroshield run --attack noise --duration 10
    python -m neuroshield web --port 7777
    python -m neuroshield info
"""

import argparse
import sys
import os

# Ensure the project root is in Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="neuroshield",
        description="NeuroShield — Virtual Neurosecurity Laboratory"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # --- neuroshield run ---
    run_parser = subparsers.add_parser("run", help="Run a simulation experiment")
    run_parser.add_argument("config_file", nargs="?", default=None,
                            help="Path to a TOML experiment config file")
    run_parser.add_argument("--duration", type=float, default=10.0)
    run_parser.add_argument("--board", type=str, choices=["synthetic", "pieeg", "cyton", "ganglion", "muse", "emotiv"], default="synthetic")
    run_parser.add_argument("--serial-port", type=str, default="", help="Serial port for physical OpenBCI boards (e.g., /dev/ttyUSB0 or COM3)")
    run_parser.add_argument("--dataset", type=str, default=None)
    run_parser.add_argument("--attack", type=str, default="")
    run_parser.add_argument("--noise-val", type=float, default=50.0)
    run_parser.add_argument("--drift-val", type=float, default=20.0)
    run_parser.add_argument("--spike-val", type=float, default=150.0)
    run_parser.add_argument("--attenuation-val", type=float, default=0.05)
    run_parser.add_argument("--report-prefix", type=str, default="neuroshield_run")
    run_parser.add_argument("--interval", type=float, default=0.1)
    run_parser.add_argument("--emulate-openbci", action="store_true")
    run_parser.add_argument("--emulate-ble", action="store_true")
    run_parser.add_argument("--ble-attack", type=str, default="")
    run_parser.add_argument("--dbs-mode", action="store_true")
    run_parser.add_argument("--dbs-attack", type=str, default="")
    run_parser.add_argument("--secure-mode", action="store_true")
    run_parser.add_argument("--nsp", action="store_true", help="Enable Neural Sensory Protocol (NSP) post-quantum cryptographic wrapper")
    run_parser.add_argument("--hardware-loopback", action="store_true")
    run_parser.add_argument("--no-report", action="store_true")
    run_parser.add_argument("--lsl", action="store_true", help="Bypass Web UI and push data to Lab Streaming Layer (LSL)")
    run_parser.add_argument("--seed", type=int, default=None,
                            help="Random seed for deterministic reproducibility")

    # --- neuroshield web ---
    web_parser = subparsers.add_parser("web", help="Launch the browser-based Web UI")
    web_parser.add_argument("--port", type=int, default=7777)
    web_parser.add_argument("--no-browser", action="store_true",
                            help="Don't auto-open browser")
    web_parser.add_argument("--board", type=str, choices=["synthetic", "pieeg", "cyton", "ganglion", "muse", "emotiv"], default="synthetic")
    web_parser.add_argument("--dbs-mode", action="store_true")
    web_parser.add_argument("--secure-mode", action="store_true")
    web_parser.add_argument("--nsp", action="store_true", help="Enable Neural Sensory Protocol (NSP) post-quantum cryptographic wrapper")
    web_parser.add_argument("--dataset", type=str, default=None)
    web_parser.add_argument("--seed", type=int, default=None)
    web_parser.add_argument("--lsl", action="store_true", help="Bypass Web UI and push data to Lab Streaming Layer (LSL)")

    # --- neuroshield info ---
    subparsers.add_parser("info", help="Display platform information and registered plugins")

    return parser


def cmd_run(args):
    """Execute a simulation experiment."""
    from neuroshield.core.config import ExperimentConfig, load_config, config_from_cli_args
    from neuroshield.core.coordinator import Coordinator

    # Load from TOML file or build from CLI args
    if args.config_file and os.path.exists(args.config_file):
        print(f"[NeuroShield] Loading experiment config: {args.config_file}")
        config = load_config(args.config_file)
        # Allow CLI seed override
        if args.seed is not None:
            config.seed = args.seed
    else:
        config = config_from_cli_args(args)
        if args.seed is not None:
            config.seed = args.seed

    coordinator = Coordinator(config)
    coordinator.setup()
    coordinator.run()
    coordinator.teardown()


def cmd_web(args):
    """Launch the web UI."""
    from neuroshield.core.config import ExperimentConfig
    from neuroshield.core.coordinator import Coordinator

    config = ExperimentConfig()
    config.web.enabled = True
    config.web.port = args.port
    config.web.open_browser = not args.no_browser
    config.web.lsl_only = args.lsl
    config.emulation.dbs_mode = args.dbs_mode
    config.security.enabled = args.secure_mode
    config.security.nsp_enabled = args.nsp
    config.dataset.path = args.dataset
    config.output.no_report = True
    if args.seed is not None:
        config.seed = args.seed

    coordinator = Coordinator(config)
    coordinator.setup()
    coordinator.run()
    coordinator.teardown()


def cmd_info(_args):
    """Display platform info."""
    from neuroshield.core.plugin_registry import PluginRegistry, register_builtin_plugins

    print("=" * 60)
    print(" NeuroShield — Virtual Neurosecurity Laboratory")
    print("=" * 60)
    print(f" Version: 0.2.0")
    print(f" Python:  {sys.version.split()[0]}")
    print()

    registry = PluginRegistry()
    register_builtin_plugins(registry)

    for category in sorted(registry.list_categories()):
        plugins = registry.list_category(category)
        print(f" [{category}]")
        for p in plugins:
            print(f"   • {p.name:20s} {p.description}")
        print()

    print("=" * 60)


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(0)

    if args.command == "run":
        cmd_run(args)
    elif args.command == "web":
        cmd_web(args)
    elif args.command == "info":
        cmd_info(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
