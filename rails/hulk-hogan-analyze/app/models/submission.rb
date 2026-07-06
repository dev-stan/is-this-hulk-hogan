class Submission < ApplicationRecord
  belongs_to :battle
  has_one_attached :photo
end
