namespace :battles do
  desc "Stub MlClient.compare for development without real ML API"
  task stub_ml: :environment do
    class Battles::MlClient
      class << self
        def compare(image_io)
          {
            similarity_score: rand(0.5..0.99).round(2),
            confidence: 0.95
          }
        end
      end
    end
    puts "MlClient stubbed with random similarity scores"
  end
end
