import yaml
from segmentation.io import read_data, write_data
from segmentation.features import wrangle_data
from segmentation.model import compute_rfm_scores, assign_segment
from config import RAW_DIR, MART_DIR, DEFAULT_CONFIG_PATH

RAW = RAW_DIR / 'synthetic_customers.csv'
OUT = MART_DIR / 'customer_segments.parquet'

def load_segmentation_rules():
    with open(DEFAULT_CONFIG_PATH) as f:
        cfg = yaml.safe_load(f)
    return cfg['segmentation']

def run():
    print('Reading csv file...')
    df = read_data(RAW)

    print('Processing data...')
    df = wrangle_data(df)

    print('Segmenting data...')
    rules = load_segmentation_rules()
    df = compute_rfm_scores(df)
    df['segment'] = df.apply(lambda r: assign_segment(r, rules), axis=1)

    print('Writing output file...')
    write_data(df, OUT)

if __name__ == "__main__":
    run()