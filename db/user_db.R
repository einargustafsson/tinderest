library(jsonlite)
library(babynames)
library(dplyr)

allergies <- c('shellfish', 'milk', 'eggs', 'nuts', 'soy', 'wheat', 'corn')
vaccinations <- c("Cholera", "Dengue", "Diphtheria", "Hepatitis A", "Hepatitis B", "Hepatitis E", "Haemophilus influenzae type b (Hib)", "Human papillomavirus (HPV)", "Influenza", "Japanese encephalitis", "Malaria", "Measles", "Meningococcal meningitis", "Mumps", "Pertussis", "Pneumococcal disease", "Poliomyelitis", "Rabies", "Rotavirus", "Rubella", "Tetanus", "Tick-borne encephalitis", "Tuberculosis", "Typhoid", "Varicella", "Yellow Fever")
mumbai_restaurants <- fromJSON('db/mumbai_restaurants.json')
restaurants <- mumbai_restaurants$results$name

pick_from_list <- function(list, min, max, replace = F) {
  d <- sample(list, floor(runif(1, min*2, max*2)/2), replace = replace)
}

make_user <- function() {
  l <- list()
  l$key <- round(runif(1, 0, 1)*1e12)
  l$agegroup <- sample(1:4, 1)
  l$health <- list(
    allergies = pick_from_list(allergies, 0, 2),
    vaccinations = pick_from_list(vaccinations, 2, 7)
  )
  l$restaurantVisits = pick_from_list(restaurants, 0, 10, replace = T)
  return(l)
}

users <- 1000
user_db <- list()
for (i in 1:users) {
  user_db[[i]] <- make_user()
}

cat(toJSON(user_db), file = sprintf('user_db_%i.json', users))
