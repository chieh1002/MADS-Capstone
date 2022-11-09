def clean_data_flavor(csv_file):
  df = pd.read_csv(csv_file)
  df['flavors'] = df['flavors'].apply(lambda x: dict(zip(re.findall('\'group\W*(.*?)\W', x), re.findall('stats\W*\'count\W*(.*?)\W', x))))
  
  data_dict = df['flavors'].to_list()
  data_dict = [dict([a, int(x)] for a, x in b.items()) for b in data_dict]

  dictvectorizer = DictVectorizer(sparse=False)
  features = dictvectorizer.fit_transform(data_dict)

  feature_name =dictvectorizer.get_feature_names()

  df_flavor = pd.DataFrame(features, columns=feature_name)

  #merge two dataframe
  cleaned_wine = pd.merge(df,df_flavor, left_index=True, right_index=True)
  cleaned_wine = cleaned_wine.drop(columns=['flavors'])

  #normalize the value of flavors by dividing ratings_count
  flavors = ['black_fruit', 'citrus_fruit', 'dried_fruit', 'earth', 'floral',
         'microbio', 'non_oak', 'oak', 'red_fruit', 'spices', 'tree_fruit',
         'tropical_fruit', 'vegetal']
  for flavor in flavors:
      cleaned_wine[flavor] = cleaned_wine[flavor]/cleaned_wine['ratings_count']
      
  return cleaned_wine
