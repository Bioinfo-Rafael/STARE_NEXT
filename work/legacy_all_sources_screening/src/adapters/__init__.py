from src.adapters.aist_well import AistWellAdapter
from src.adapters.ebird import EBirdAdapter
from src.adapters.firms import FirmsAdapter
from src.adapters.gbif import GbifAdapter
from src.adapters.gdelt import GdeltAdapter
from src.adapters.glotec import GlotecAdapter
from src.adapters.google_trends import GoogleTrendsAdapter
from src.adapters.inaturalist import INaturalistAdapter
from src.adapters.kp_dst import KpDstAdapter
from src.adapters.movebank import MovebankAdapter
from src.adapters.openaq import OpenAqAdapter
from src.adapters.opensky import OpenSkyAdapter
from src.adapters.tepco import TepcoAdapter
from src.adapters.wikimedia import WikimediaAdapter

EXTERNAL_ADAPTERS = {
    "google_trends": GoogleTrendsAdapter,
    "wikimedia": WikimediaAdapter,
    "gdelt": GdeltAdapter,
    "glotec": GlotecAdapter,
    "kp_dst": KpDstAdapter,
    "aist_well": AistWellAdapter,
    "movebank": MovebankAdapter,
    "ebird": EBirdAdapter,
    "inaturalist": INaturalistAdapter,
    "gbif": GbifAdapter,
    "openaq": OpenAqAdapter,
    "firms": FirmsAdapter,
    "tepco": TepcoAdapter,
    "opensky": OpenSkyAdapter,
}
