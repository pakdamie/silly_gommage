give_age_individual <- function(wrangled_dat){

  #Total population size 
  n = wrangled_dat$pop_size[1]

  #This is the population that we want to make for the city of interest
  pop <- data.frame(x = runif(n, min = -500000, max = 500000),
                    y = runif(n, min = -500000, max = 500000),
                    id = seq(1,n))

  #Of a particular age, repeat that "age-identity" some number of times
  # depending on the number of members within this age group 
  age_list_column = NULL        
  for (age_group in 1:101){
    age_interest <- wrangled_df_r[age_group + 1, "numbers"]
    pop_size <- wrangled_df_r[age_group + 1, "pop_size"]
    age_list_column[[age_group]] = rep(age_interest, pop_size)
  }

  age_list_col_df <- unlist(age_list_column)

  pop$age <- age_list_col_df
  pop$alive <- "A"
  pop$time_gommage = ceiling((100 - pop$age)/2)

  ###Now make it into animation slide
  animation_slide = NULL
  
  for (anim_slide in 1:100){
    
    #Age group of interest (remember it goes from 100 to 1)
    
     #Start at 2 so that the 
    df_anim_slide <- cbind(time = anim_slide,pop)
    df_anim_slide$alive <- ifelse(df_anim_slide$time_gommage < anim_slide , "D","A")
    animation_slide[[anim_slide]] <-  df_anim_slide
  }

  anim_df <- do.call(rbind, animation_slide)
  anim_df <- rbind(cbind(time = 1,pop), anim_df)
  anim_df <- subset(anim_df, anim_df$alive == "A")

  return(anim_df)

}

