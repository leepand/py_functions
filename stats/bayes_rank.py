import pandas as pd
from scipy.stats import beta

# https://medium.com/airy-science/search-ranking-with-bayesian-inference-608275e36ee
# Example, you could use this when you want to compare items in marketplace. Feel free to change or add the data and re-run.
max_score = 5.0
# rows of tuple (name, number of review, average review score)
review_data = pd.DataFrame(
    [["Item A", 2, 5], ["Item B", 300, 4.8], ["Item C", 50, 4.64]],
    columns=["name", "review_count", "review_score"],
)

# Functions
def get_beta_dist(average_score, max_score, review_count):
    success = (float(average_score) / float(max_score)) * review_count
    failure = review_count - success
    uniform_prior = 1.0
    dist_alpha = uniform_prior + success
    dist_beta = uniform_prior + failure
    return beta(dist_alpha, dist_beta)


def bayesian_rank(max_score, review_data):
    review_data_rank = review_data.copy(deep=False)

    lower_beta_list = []
    for index, item in review_data_rank.iterrows():
        beta_dist = get_beta_dist(item["review_score"], max_score, item["review_count"])
        # Get the lower_beta from probability density function where x < lower_beta
        # contains 0.05 area of distribution and 0.95 area for x > lower_beta
        lower_beta = beta_dist.ppf(0.05)
        lower_beta_list.append(lower_beta)

    review_data_rank["lower_beta"] = lower_beta_list
    review_data_rank["rank"] = review_data_rank["lower_beta"].rank(
        method="min", ascending=False
    )

    return review_data_rank.sort_values(by="rank")


# Print the result by using provided data
print("\n")
print(
    "Feel free to change the max_score and review_data then re-run. Or you could use bayesian_rank function from terminal.\n"
)
print(bayesian_rank(max_score, review_data))
print("\n")
