class Avo::Resources::User < Avo::BaseResource
  self.title = :id
  self.includes = []
  # self.search_query = -> do
  #   query.ransack(id_eq: params[:q], m: "or").result(distinct: false)
  # end

  def fields
    field :id, as: :id
  field :email, as: :text
  field :name, as: :text
  end

  action Avo::Actions::ToggleInactive
end
