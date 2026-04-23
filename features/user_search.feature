Feature: GitHub user search
  As a user of the app
  I want to search for GitHub users
  So that I can view profile details

  @ui @api @happy-path
  Scenario: Search swangful and verify 17 repositories
    Given I open the GitHub user search application
    When I search for github user "swangful"
    And I open "swangful" from the results
    Then I should see "swangful" profile details
    And I should see 17 repositories in the UI
    And the API should report 17 repositories for "swangful"
