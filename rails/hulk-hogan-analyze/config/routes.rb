Rails.application.routes.draw do
  get "up" => "rails/health#show", as: :rails_health_check

  root "battles#new"

  resources :battles, only: [:new, :create, :show] do
    member do
      get  :waiting
      get  :join
      post :submit
      get  :result
    end
  end
end
