def euc_2d(c1, c2)
  Math.sqrt((c1[0] - c2[0])**2.0 + (c1[1] - c2[1])**2.0).round
end

def cost(perm, cities)
  distance =0
  perm.each_with_index do |c1, i|
    c2 = (i==perm.size-1) ? perm[0] : perm[i+1]
    distance += euc_2d(cities[c1], cities[c2])
  end
  return distance
end

def random_permutation(cities)
  perm = Array.new(cities.size){|i| i}
  perm.each_index do |i|
    r = rand(perm.size-i) + i
    perm[r], perm[i] = perm[i], perm[r]
  end
  return perm
end

def stochastic_two_opt!(perm)
  c1, c2 = rand(perm.size), rand(perm.size)
  exclude = [c1]
  exclude << ((c1==0) ? perm.size-1 : c1-1)
  exclude << ((c1==perm.size-1) ? 0 : c1+1)
  c2 = rand(perm.size) while exclude.include?(c2)
  c1, c2 = c2, c1 if c2 < c1
  perm[c1...c2] = perm[c1...c2].reverse
  return perm
end

def local_search(best, cities, max_no_improv, neighborhood)
  count = 0
  begin
    candidate = {}
    candidate[:vector] = Array.new(best[:vector])
    neighborhood.times{stochastic_two_opt!(candidate[:vector])}
    candidate[:cost] = cost(candidate[:vector], cities)
    if candidate[:cost] < best[:cost]
      count, best = 0, candidate
    else
      count += 1
    end
  end until count >= max_no_improv
  return best
end

def search(cities, neighborhoods, max_no_improv, max_no_improv_ls)
  best = {}
  best[:vector] = random_permutation(cities)
  best[:cost] = cost(best[:vector], cities)
  iter, count = 0, 0
  begin
    neighborhoods.each do |neigh|
      candidate = {}
      candidate[:vector] = Array.new(best[:vector])
      neigh.times{stochastic_two_opt!(candidate[:vector])}
      candidate[:cost] = cost(candidate[:vector], cities)
      candidate = local_search(candidate, cities, max_no_improv_ls, neigh)
      #puts " > iteration #{(iter+1)}, neigh=#{neigh}, best=#{best[:cost]}"
      iter += 1
      if(candidate[:cost] < best[:cost])
        best, count = candidate, 0
        puts "New best, restarting neighborhood search."
        break
      else
        count += 1
      end
    end
  end until count >= max_no_improv
  return best
end
############################################################
if __FILE__ == $0
  ERRO = [[1,1],[2,2]]
############################################################
   contentsArray = Array.new
   points = Array.new
   file_name = ENV['file_name']
   file = File.open(file_name, "r")
   file.each_line { |line|
    valores = (line.split())
    a = valores[1].to_f
    b =  valores[2].to_f
    contentsArray = [a, b]
    points.push(contentsArray)
   }
  #antes era 50	
  max_no_improv = 225 * 2
  ##550
  #antes era 70
  max_no_improv_ls = 375 * 2
  ##770
  #antes era 20
  neighborhoods = 1...75
  #100
  ##90
  # execute the algorithm
  best = search(points, neighborhoods, max_no_improv, max_no_improv_ls)
  puts "Done. Best Solution: c=#{best[:cost]}, v=#{best[:vector].inspect}"
  file_text = "#{best[:cost]}\n#{best[:vector].inspect}"
  File.write('best.txt',file_text , mode: 'w')
end
