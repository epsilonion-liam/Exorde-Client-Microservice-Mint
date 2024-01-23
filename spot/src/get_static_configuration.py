from get_contracts import get_contracts
from read_web3 import read_web3 as _read_web3
from write_web3 import write_web3 as _write_web3
from get_worker_account import get_worker_account
from get_protocol_configuration import get_protocol_configuration
from get_contracts_and_abi_cnf import get_contracts_and_abi_cnf
from get_network_configuration import get_network_configuration
from models import StaticConfiguration
from lab_initialization import lab_initialization
import logging, os


async def do_get_static_configuration(live_configuration) -> StaticConfiguration:
    main_address: str = os.getenv('main_address', '')
    assert main_address != ''
    protocol_configuration: dict = get_protocol_configuration()
    network_configuration: dict = await get_network_configuration()
    contracts_and_abi = await get_contracts_and_abi_cnf(
        protocol_configuration, live_configuration
    )
    read_web3 = _read_web3(
        protocol_configuration, network_configuration, live_configuration
    )
    contracts = get_contracts(
        read_web3,
        contracts_and_abi,
        protocol_configuration,
        live_configuration,
    )
    worker_account = get_worker_account("some-worker-name")
    gas_cache = {}
    write_web3 = _write_web3(
        protocol_configuration, network_configuration, live_configuration
    )
    lab_configuration = lab_initialization()
    return StaticConfiguration(
        main_address=main_address,
        worker_account=worker_account,
        protocol_configuration=protocol_configuration,
        network_configuration=network_configuration,
        contracts=contracts,
        contracts_and_abi=contracts_and_abi,
        read_web3=read_web3,
        write_web3=write_web3,
        lab_configuration=lab_configuration,
        gas_cache=gas_cache,
    )


async def get_static_configuration(live_configuration) -> StaticConfiguration:
    try:
        static_configuration: StaticConfiguration = (
            await do_get_static_configuration(live_configuration)
        )
        return static_configuration
    except:
        logging.exception(
            "An error occured retrieving static configuration, exiting"
        )
        os._exit(1)
