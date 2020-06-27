import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """
    
    # We define a queue == breadth-first search
    queue = QueueFrontier()
    exploredSet = list()

    # We're going to look neighbors 
    node = Node(source, None, None)
    exploredSet.append(source)
    neighbors = neighbors_for_person(source)
    
    # If doesn't has any neighbor, return None (there are people that has done just one movie of 1 actor)
    if len(neighbors) == 0:
        return None
    
    # For each neighbor, add to the queue each possible action (walk through the movie)
    for i in neighbors:
        node = Node(state = i[1], parent = None, action = i[0])
        queue.add(node)
    # Check if we found the target
    if queue.contains_state(target):
        node = queue.search_state(target)
        return [(node.getAction(), target)]

    # took out an element from the queue and walk through the neighboors
    while not queue.empty():

        parent = queue.remove() 

        """ This is not necesary, because i found an eficient implementation checking if we reached the target when
        we add a node, and not when we remove it...

        if parent.getState() == target:
            # Once we have the target, go backwards. FIFO will be useful to do the path till the target
            result = StackFrontier()
            # Add the target element and go backward till the beginning through the parents
            result.add(parent)
            node = parent.getParent()
            while node != None:
                result.add(node)
                node = node.getParent()
            # build the return list in the correct order taking out every stack element
            r = list()
            while not result.empty():
                node = result.remove()
                movie = node.getAction()
                person = node.getState()
                r.append([movie, person])
            return r
        """
        
        # Add the node to the explore dataset because we don't want to walk through the same way that we came
        exploredSet.append(parent.getState())

        # expand the node and find neighbors
        neighbors = neighbors_for_person(parent.getState())  # remember state == person

        # For each neighbor we have the name of the neighbor i[1] and the movie i[0] shared with the parent of the neighbor
        for i in neighbors:
            node = Node(state=i[1], parent=parent, action=i[0]) #  action == movies

            # If we have been in this neighbor before (this person), continue and don't expand this node again
            if queue.contains_state(node.getState()) or node.getState() in exploredSet:
                continue
            queue.add(node)

            # Check if this node has the target
            if node.getState() == target:
                # Once we have the target, go backwards. FIFO will be useful for this
                result = StackFrontier()
                # add the target element and go backward till the beginning through the parents
                result.add(node)
                node = node.getParent()
                while node != None:
                    result.add(node)
                    node = node.getParent()
                # build the return list in the correct order taking out every stack element
                r = list()
                while not result.empty():
                    node = result.remove()
                    movie = node.getAction()
                    person = node.getState()
                    r.append([movie, person])
                return r
        

    # raise NotImplementedError
    return None


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
