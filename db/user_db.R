library(jsonlite)
library(dplyr)
library(utils)
set.seed(12333)

# Subset of allergies and vaccinations ------------------------------------
allergies <- c('shellfish', 'milk', 'peanuts') # 'nuts', 'soy', 'wheat', 'corn')
vaccinations <- c("Cholera", "Dengue", "Diphtheria", "Hepatitis A", "Hepatitis B", "Hepatitis E", "Haemophilus influenzae type b (Hib)", "Human papillomavirus (HPV)", "Influenza", "Japanese encephalitis", "Malaria", "Measles", "Meningococcal meningitis", "Mumps", "Pertussis", "Pneumococcal disease", "Poliomyelitis", "Rabies", "Rotavirus", "Rubella", "Tetanus", "Tick-borne encephalitis", "Tuberculosis", "Typhoid", "Varicella", "Yellow Fever")


# Restaurants in Mumbai ---------------------------------------------------

# Get Restaurants from the Google Places API
if (!exists('google_api_key')) google_api_key <- readline('insert api-key')
mumbai_places <- paste0('https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=19.0613878,72.8604882&radius=500&types=food&name=restaurant&key=', google_api_key) %>% 
  utils::URLencode() %>% 
  fromJSON()
mumbai_restaurants <- mumbai_places$results

# Flatten json-lists to have a clean table
mumbai_restaurants$geometry <- paste(unlist(mumbai_restaurants$geometry), collapse=',')
mumbai_restaurants$opening_hours <- paste(unlist(mumbai_restaurants$opening_hours), collapse=',')


# Functions ---------------------------------------------------------------
pick_from_list <- function(list, min, max, replace = F) {
  d <- sample(list, floor(runif(1, min*2, max*2)/2), replace = replace)
  return(d)
}

pick_restaurants <- function(restaurants, allergies, min, max) {
  if (length(allergies) > 0) {
    safe <- grepl(allergies, restaurants$allergySafe)
    picks <- restaurants[safe, 'name']
  } else {
    picks <- restaurants[ ,'name']
  }  
    if (length(picks) < 1) return('')
    pick_from_list(picks, min, max, replace = T)
}

make_user <- function(allergies, vaccinations, restaurants) {
  user <- list()
  user$key <- round(runif(1, 0, 1)*1e12)
  user$agegroup <- sample(1:4, 1)
  user$health <- list(
    allergies = pick_from_list(allergies, 0, 2),
    vaccinations = pick_from_list(vaccinations, 2, 7)
  )
  user$financeCategory <- sample(1:4, 1)
  if (!is.null(nrow(restaurants))) {
    user$restaurantVisits <- pick_restaurants(restaurants, 
                                              user$health$allergies, 
                                              2, 10)
  }
  return(user)
}


# Generate data -----------------------------------------------------------

# Set restaurant allergy constraints to be able simulate restaurant visits
for (i in seq_along(mumbai_restaurants)) {
  mumbai_restaurants$allergySafe[i] <- paste(pick_from_list(allergies, 0, 3), collapse = ',')
}

# Create n users and export to json
users <- 1000
user_db <- list()
for (i in 1:users) {
  user_db[[i]] <- make_user(allergies, 
                            vaccinations, 
                            mumbai_restaurants)
}
cat(toJSON(user_db), file = sprintf('db/user_db_%i.json', users))

# Create one app user
app_user <- make_user(allergies, vaccinations, restaurants = NA)
cat(toJSON(app_user), file = 'db/app_user.json')

