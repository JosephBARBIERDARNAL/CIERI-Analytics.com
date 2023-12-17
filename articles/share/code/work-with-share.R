#install.packages('dplyr')
#install.packages('foreign')

rm(list=ls())
library('dplyr')
library('foreign')
library('forcats')

br_dataframe = read.dta('../SHARE/data/sharew6_rel8-0-0_ALL_datasets_stata/sharew6_rel8-0-0_br.dta')
dn_dataframe = read.dta('../SHARE/data/sharew6_rel8-0-0_ALL_datasets_stata/sharew6_rel8-0-0_dn.dta')
ph_dataframe = read.dta('../SHARE/data/sharew6_rel8-0-0_ALL_datasets_stata/sharew6_rel8-0-0_ph.dta')

merged_dataframe = merge(br_dataframe, dn_dataframe, by = 'mergeid') 
merged_dataframe = merge(merged_dataframe, ph_dataframe, by = 'mergeid')

df = merged_dataframe %>%
        select(contains('dn014_'), contains('dn042_'),
               contains('br002_'), contains('br015_'),
               contains('ph003_'), contains('ph084_'),
               contains('dn003_'))

df = df %>%
        rename(
          MaritalStatus = dn014_,
          Gender = dn042_,
          YearOfBirth = dn003_,
          Smoking = br002_,
          SportFrequency = br015_,
          HealthSelfPerception = ph003_,
          Pain = ph084_
        )

values_to_replace = c("Don't know", "Refusal",
                      "Implausible value/suspected wrong",
                      "Not codable", "Not answered",
                      "Not yet coded", "Not applicable")      
df = df %>%
  mutate(across(everything(),
         ~if_else(. %in% values_to_replace, NA, .)))

print(str(df))

df = df %>%
    mutate(
      YearOfBirth = as.numeric(YearOfBirth),
      MaritalStatus = as.factor(MaritalStatus),
      Gender = as.factor(Gender),
      Smoking = as.factor(Smoking),
      SportFrequency = as.factor(SportFrequency),
      HealthSelfPerception = as.factor(HealthSelfPerception),
      Pain = as.factor(Pain)
    )

# Change YearOfBirth to Age
df = df %>%
    mutate(Age = 2021 - YearOfBirth) %>%
    select(-YearOfBirth)

# Change NaN in categorical columns as "Unknown"
is_categorical <- function(x) {
  is.factor(x) || is.character(x)
}
df = df %>%
    mutate(across(where(is_categorical), ~ if_else(is.na(.), "Unknown", .)))
print(head(df, 100))
#write.csv(df, 'data/share-cleaned-dataset.csv', row.names = FALSE)

