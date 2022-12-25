from dataclasses import dataclass


@dataclass
class DataIngestionArtifact:
    raw_data_path: str

    # s3_artifacts_path: str
