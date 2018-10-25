
# coding: utf-8

# In[ ]:


#Lets create a list of unique values in friends column
friends_list = school_dataset["friends"].unique().tolist()
print("Lets print the distribution of number of friends")
for f in friends_list:
    print("Number of samples which have", f,"friends:", len(school_dataset[school_dataset["friends"].str.contains(f)]))


#lets create a list of unique values in gender column
gender_list = school_dataset["gender"].unique().tolist()
gender_list
print("Lets print the distribution with respect to gender")
for g in gender_list:
    print("Number of students from", g,"gender:", len(school_dataset[school_dataset["gender"].str.contains(g)]))

#loop through gender_list and friends_list to find the people of particular gender have what number of friends
print("Lets print the gender breakdown of friends")
for g in gender_list:
    for f in friends_list:
        x = np.where((school_dataset["gender"] ==g) & (school_dataset['friends'] == f))
        print("Number of", g, "students which have",f,"friends:", len(x[0]))
#lets make one more list of unique values in race column
print("Lets print the distribution of student by race")
race = school_dataset["race"].unique().tolist()
for r in race:
    print("Number of students from", r,"background:", len(school_dataset[school_dataset["race"].str.contains(r)]))

print("Lets print the breakdown by race of number of friends students have ")
#loop through race and friends_list to find the people of particular race have what number of friends
for r in race:
    for f in friends_list:
        x = np.where((school_dataset["race"] ==r) & (school_dataset['friends'] == f))
        print("Number of students from", r, "background which have",f,"friends:", len(x[0]))

