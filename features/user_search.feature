Feature: GitHub user search
  As a user of the app
  I want to search for GitHub users
  So that I can view profile details

  @ui @api @happy-path
  Scenario: Search swangful and verify UI repo count matches GitHub
    Given I open the GitHub user search application
    When I search for github user "swangful"
    And I open "swangful" from the results
    Then I should see "swangful" profile details
    And the UI repository count should match GitHub public_repos for "swangful"
