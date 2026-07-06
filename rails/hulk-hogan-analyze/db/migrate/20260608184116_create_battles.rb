class CreateBattles < ActiveRecord::Migration[8.1]
  def change
    create_table :battles do |t|
      t.string :share_token, null: false
      t.integer :status, default: 0

      t.timestamps
    end
    add_index :battles, :share_token, unique: true
  end
end
