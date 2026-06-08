class BattlesController < ApplicationController
  before_action :set_battle, only: [:show, :join, :submit, :result]

  def new
    @battle = Battle.new
  end

  def create
    @battle = Battle.create!(status: :waiting_for_p2)
    @submission = @battle.submissions.build(player_number: 1)
    @submission.photo.attach(params[:photo])

    begin
      result = Battles::MlClient.compare(@submission.photo.download)
      @submission.similarity_score = result[:similarity_score]
      @submission.processed_at = Time.current
      @submission.save!
    rescue Battles::MlClient::FaceNotDetected
      flash[:error] = "No face detected, try another photo"
      return redirect_to new_battle_path
    rescue Battles::MlClient::ApiError => e
      flash[:error] = "ML service unavailable, try again"
      return redirect_to new_battle_path
    end

    redirect_to waiting_battle_path(@battle)
  end

  def show
    @submission = @battle.submissions.find_by(player_number: 1)
    redirect_to waiting_battle_path(@battle)
  end

  def waiting
    @submission = @battle.submissions.find_by(player_number: 1)
  end

  def join
  end

  def submit
    @submission = @battle.submissions.build(player_number: 2)
    @submission.photo.attach(params[:photo])

    begin
      result = Battles::MlClient.compare(@submission.photo.download)
      @submission.similarity_score = result[:similarity_score]
      @submission.processed_at = Time.current
      @submission.save!
    rescue Battles::MlClient::FaceNotDetected
      flash[:error] = "No face detected, try another photo"
      return redirect_to join_battle_path(@battle)
    rescue Battles::MlClient::ApiError => e
      flash[:error] = "ML service unavailable, try again"
      return redirect_to join_battle_path(@battle)
    end

    @battle.update!(status: :completed)
    redirect_to result_battle_path(@battle)
  end

  def result
    @submission_1 = @battle.submissions.find_by(player_number: 1)
    @submission_2 = @battle.submissions.find_by(player_number: 2)
  end

  private

  def set_battle
    @battle = Battle.find_by!(share_token: params[:id])
  end
end
