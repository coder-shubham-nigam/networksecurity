import os

from Network_Security.components.data_ingestion import DataIngestion
from Network_Security.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig


def test_export_collection_as_dataframe_uses_local_csv_when_mongo_unavailable(monkeypatch):
    monkeypatch.setenv("MONGO_DB_URL", "mongodb+srv://invalid:wrong@cluster0.example.mongodb.net/?retryWrites=true&w=majority")

    training_pipeline_config = TrainingPipelineConfig()
    data_ingestion_config = DataIngestionConfig(training_pipeline_config)
    data_ingestion = DataIngestion(data_ingestion_config)

    df = data_ingestion.export_collection_as_dataframe()

    assert "Result" in df.columns
    assert not df.empty
