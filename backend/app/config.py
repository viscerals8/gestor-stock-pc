from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    db_server: str
    db_port: int = 1433
    db_name: str
    db_user: str
    db_password: str
    db_driver: str = "ODBC Driver 17 for SQL Server"

    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 480

    admin_nombre: str = "Administrador"
    admin_correo: str = "admin@empresa.com"
    admin_password: str = "changeme"

    seed_tecnico_password: str = "changeme"

    cors_origins: str = "http://localhost:8100,http://localhost:4200"

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    @property
    def sqlalchemy_database_url(self) -> str:
        driver = self.db_driver.replace(" ", "+")
        return (
            f"mssql+pyodbc://{self.db_user}:{self.db_password}"
            f"@{self.db_server}:{self.db_port}/{self.db_name}"
            f"?driver={driver}&Encrypt=yes&TrustServerCertificate=yes"
        )

    @property
    def sqlalchemy_master_url(self) -> str:
        """URL apuntando a 'master', usada solo por scripts/init_db.py para crear la base."""
        driver = self.db_driver.replace(" ", "+")
        return (
            f"mssql+pyodbc://{self.db_user}:{self.db_password}"
            f"@{self.db_server}:{self.db_port}/master"
            f"?driver={driver}&Encrypt=yes&TrustServerCertificate=yes"
        )


settings = Settings()
