module Battles
  class MlClient
    def self.compare(image_io)
      {
        similarity_score: rand(0.5..0.99).round(2),
        confidence: 0.95
      }
    end
  end
end
