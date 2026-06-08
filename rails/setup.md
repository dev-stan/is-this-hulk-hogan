Work file by file. Run migrations after generating models. Show me errors before proceeding.

You are a senior Rails developer. Help me build a face comparison web app fast. 
No unnecessary questions — make sensible decisions and tell me what you chose.

## Context
Rails app already initialized. Build on top of it.
Goal: user uploads a photo, a ML API compares it to Hulk Hogan, returns a similarity score.
Two players can compete via a share link. No auth, no accounts.

## Stack decisions (do not deviate)
- Rails 7, Hotwire/Turbo (already included)
- ActiveStorage for photo uploads (configure for local disk)
- `http` gem for ML API calls
- Tailwind if available, otherwise plain CSS — do not install new UI frameworks
- No Sidekiq, no background jobs — synchronous ML calls only

## Domain model — generate these exactly

### Battle
- share_token: string (uuid, non-nullable, indexed, unique)
- status: integer enum — waiting_for_p2 (0), processing (1), completed (2)
- timestamps

### Submission
- battle_id: references
- player_number: integer (1 or 2)
- similarity_score: float (nullable until ML responds)
- processed_at: datetime (nullable)
- timestamps
- has_one_attached :photo

## File structure to create

app/
  domains/
    battles/
      ml_client.rb
      battle_creator.rb
  controllers/
    battles_controller.rb
  views/
    battles/
      new.html.erb        # player 1 upload form
      waiting.html.erb    # player 1 waits for player 2
      join.html.erb       # player 2 upload form
      result.html.erb     # both scores revealed

## ML API contract (hardcode this, do not invent alternatives)

POST to ENV["ML_API_URL"] + "/compare"

Request body (JSON):
{
  "image_base64": "<base64 string>",
  "reference": "hulk_hogan"
}

Success response:
{
  "similarity_score": 0.84,
  "confidence": 0.91
}

Error response:
{
  "error": "face_not_detected",
  "message": "No face found in image"
}

## MlClient implementation

class Battles::MlClient
  BASE_URL = ENV.fetch("ML_API_URL", "http://localhost:5000")

  def self.compare(image_io)
    b64 = Base64.strict_encode64(image_io.read)
    response = HTTP.timeout(10)
                   .post("#{BASE_URL}/compare", json: { image_base64: b64, reference: "hulk_hogan" })

    raise Battles::MlClient::FaceNotDetected if response.status == 422
    raise Battles::MlClient::ApiError, response.status unless response.status.ok?

    response.parse.deep_symbolize_keys
  end

  class FaceNotDetected < StandardError; end
  class ApiError < StandardError; end
end

## Routes

resources :battles, only: [:new, :create, :show] do
  member do
    get  :join
    post :submit
    get  :result
  end
end

## Controller logic

BattlesController#create
  - Creates Battle (status: waiting_for_p2, share_token: SecureRandom.uuid)
  - Creates Submission for player 1 (player_number: 1), attaches photo
  - Calls MlClient.compare, saves similarity_score + processed_at
  - Redirects to waiting path

BattlesController#join (GET)
  - Finds Battle by share_token (param: :id)
  - Renders join form for player 2

BattlesController#submit (POST)
  - Creates Submission for player 2 (player_number: 2), attaches photo
  - Calls MlClient.compare, saves score
  - Updates Battle status to completed
  - Redirects to result path

BattlesController#result
  - Loads both submissions
  - Renders scores side by side

## Views — keep them functional, not pretty. No inline styles, just semantic HTML.

new.html.erb     → h1 "Upload your photo", file input, submit button
waiting.html.erb → share link prominently displayed, "Waiting for your opponent..."
join.html.erb    → h1 "You've been challenged", file input, submit button
result.html.erb  → two columns: Player 1 score vs Player 2 score, winner highlighted

## Error handling in views
- Catch Battles::MlClient::FaceNotDetected → flash[:error] = "No face detected, try another photo"
- Catch Battles::MlClient::ApiError → flash[:error] = "ML service unavailable, try again"
- Redirect back to upload form on error

## Seed / test stub
Add a rake task `rails battles:stub_ml` that stubs MlClient.compare 
to return { similarity_score: rand(0.5..0.99).round(2), confidence: 0.95 } 
so we can develop without the real ML API running.

## Do not build
- User authentication
- Leaderboard
- WebSockets or ActionCable
- Background jobs
- File size validation (skip for now)
- Any animation logic

## When done, tell me:
1. Every file you created
2. The exact URL flow (new → waiting → join → result)
3. The one ENV var I need to set
4. How to run the ML stub task