class Battle < ApplicationRecord
  has_many :submissions, dependent: :destroy

  enum :status, { waiting_for_p2: 0, processing: 1, completed: 2 }

  validates :share_token, presence: true, uniqueness: true

  before_create :generate_share_token

  private

  def generate_share_token
    self.share_token = SecureRandom.uuid
  end
end
