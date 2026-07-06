class CreateSubmissions < ActiveRecord::Migration[8.1]
  def change
    create_table :submissions do |t|
      t.references :battle, null: false, foreign_key: true
      t.integer :player_number
      t.float :similarity_score
      t.datetime :processed_at

      t.timestamps
    end
  end
end
