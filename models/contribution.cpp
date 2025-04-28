#include <iostream>
#include <vector>
#include <string>
#include <stdexcept>
#include <ctime>

class Contribution {
public:
    Contribution(std::string contributor, std::time_t date, std::string details)
        : contributor(contributor), date(date), details(details) {}

    std::string getContributor() const { return contributor; }
    std::time_t getDate() const { return date; }
    std::string getDetails() const { return details; }

private:
    std::string contributor;
    std::time_t date;
    std::string details;
};

class ContributionModel {
public:
    // Assuming contributions are loaded from a database or another source
    std::vector<Contribution> contributions;

    void loadContributions() {
        // Load contributions from persistent storage (e.g., database)
        // (Stub for illustration purposes)
    }

    std::vector<Contribution> getContributionsByDate(std::time_t startDate, std::time_t endDate) {
        loadContributions();
        
        if (startDate > endDate) {
            throw std::invalid_argument("Start date must be earlier than end date");
        }

        std::vector<Contribution> result;
        for (const auto& contribution : contributions) {
            if (contribution.getDate() >= startDate && contribution.getDate() <= endDate) {
                result.push_back(contribution);
            }
        }

        return result;
    }
};
