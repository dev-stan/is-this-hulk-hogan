module Battles
  class MlClient
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
end
