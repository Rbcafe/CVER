class Avo::Actions::ToggleInactive < Avo::BaseAction
  self.name = "Toggle inactive"
  # self.visible = -> do
  #   true
  # end

  # def fields
  #   # Add Action fields here
  # end

  def handle(**args)
    error "<em>oh no</em><script>alert('boo')</script>"
  end
end
