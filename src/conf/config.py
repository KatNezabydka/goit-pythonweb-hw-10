class Config:
    DB_URL = "postgresql+asyncpg://postgres:567234@postgres:5432/contacts"
    JWT_SECRET = "xjiQi5T-_DH9sfYEJnC1Df74rHrM30Oi4PS4sM6PFNM"  # Секретний ключ для токенів
    JWT_ALGORITHM = "HS256"  # Алгоритм шифрування токенів
    JWT_EXPIRATION_SECONDS = 3600  # Час дії токена (1 година)

config = Config