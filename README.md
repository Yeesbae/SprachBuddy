# SprachBuddy

Architechture Overview Diagram
```bash
┌───────────────────────────┐
                         │        Telegram API        │
                         │  (sends webhook updates)   │
                         └──────────────┬────────────┘
                                        │ HTTPS
                                        ▼
                            ┌───────────────────────┐
                            │     Cloud Run API     │
                            │  (FastAPI/Node bot)   │
                            │  Always Free Tier     │
                            └──────────┬────────────┘
      ┌────────────────────────────────┴────────────────────────┐
      │                                                         │
      ▼                                                         ▼
┌──────────────┐                                      ┌───────────────────┐
│ Quick Reply   │                                      │ Enqueue Job       │
│ Handle small  │                                      │ to Pub/Sub Topic  │
│ commands fast │                                      │ (audio, quizzes,  │
└──────────────┘                                      │ SRS, duels etc.)   │
                                                       └───────────┬───────┘
                                                                   │
                                                   (asynchronous)  ▼
                                                      ┌──────────────────┐
                                                      │   VM Instance    │
                                                      │  (f1-micro free) │
                                                      │ Runs:            │
                                                      │ - Redis (cache)  │
                                                      │ - Worker Pool    │
                                                      │ - Duel engine    │
                                                      │ - SRS scheduler  │
                                                      └──────────┬───────┘
                                                                  │
                                             ┌────────────────────┘
                                             │
                         ┌───────────────────▼─────────────────────┐
                         │               Databases                 │
                         │                                         │
                         │ Firestore (free tier)                   │
                         │ - user profile                          │
                         │ - streaks & XP                          │
                         │ - vocab metadata                        │
                         │                                         │
                         │ Redis (on VM, free)                     │
                         │ - leaderboards (sorted sets)            │
                         │ - session/cache                         │
                         │ - rate limits                           │
                         │                                         │
                         └──────────────────────┬──────────────────┘
                                                │
                                                ▼
                            ┌──────────────────────────┐
                            │   Cloud Storage (5GB)    │
                            │ Audio, images, TTS files │
                            │ always-free + cheap      │
                            └──────────────────────────┘
```

## Build docker image
Build the Docker image locally:
```bash
docker build -t sprachbuddy:latest .
```

Tag Docker image for Google Container Registry (GCR)
```bash
docker tag sprachbuddy:latest gcr.io/$PROJECT_ID/sprachbuddy:latest
```

Push to Google Container Registry
```bash
docker push gcr.io/$PROJECT_ID/sprachbuddy:latest
```

Deploy
```bash
gcloud run deploy sprachbuddy --image gcr.io/$PROJECT_ID/sprachbuddy:latest --platform managed --region asia-southeast1 --allow-unauthenticated --port 8080 --set-env-vars BOT_TOKEN=$BOT_TOKEN
```
