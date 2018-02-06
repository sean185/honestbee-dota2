## Honestbee Data Engineering team interview test

#### Setting Up
1. Setup virtual environment with python3 `virtualenv -p python3 <ENV_PATH>`
2. `source <ENV_PATH>/bin/activate` and `pip install requirements.txt`
3. Start `hug -f server.py`
4. Proxy-pass from nginx as necessary

#### Usage
* Currently hosted at https://seanang.me/honestbee/
* Routes are `/leaderboard`, `/compare`, and `/suggest`, described in the next section

___

### Technical Questions

#### 1. Leaderboard
_Given a list of player(s) (either player_id or username and assuming all players have a Dota2 public profile), return a leaderboard of the players based on their win rate over time (last week, last month, last year...)._

**route:** `/leaderboard`
  * player_ids - a comma separated list of account_ids / usernames
  * time_frame - ('week'/'month'/'year'), maps to values (7/30/365)

e.g `/leaderboard?player_ids=76482434,4294967295&time_frame=month`

**response:**
> Array of player objects
> - account_id
> - win_rate
> - wins (absolute)

#### 2. Comparison
_Given two players, return a comparison between the two players. The attributes of the players for comparison can be at your choice._

**route:** `/compare`
  * player_A - the first player's account_id / username
  * player_B - the second player's account_id / username

e.g `/compare?player_A=76482434&player_B=4294967295`

**response:**
> Object of comparison fields with the better player as the value

#### 3. Suggestion
_Given one player, return a suggestion of a hero that one player should play based on the player's historical data._

**route:** `/suggest`
  * player - the player's account_id / username

e.g `/suggest?player=76482434`

**response:**
> A single hero name suggestion

#### Caveats:
  * account_id is inferred from username via the API https://api.opendota.com/api/search, which guesses by personaname. This is not accurate as multiple accounts may have the same personaname.

___

### Write-up & Explanation

#### 1. Choice of stack

  * Hug - http://www.hug.rest/

At the moment the requirements are still vague and I did not want to put in unnecessary work without a clear product in mind.
Hug allowed for quick and sensible prototyping of APIs while providing failsafes and catches automatically.

**Pros of Hug**
  * clear syntax and straightforward use of decorators, compared to Twisted, Tornado, etc.
  * more featured and offers type casting and checking, compared to Web.py
  * lightweight and zero configuration required, compared to Django

**Pros of not using a DB**
  * until the product has a clear use for it, no need to add a resource overhead
  * data retrieved is always up to date

**Cons of not using a DB**
  * choosing to cache player data will overload memory usage in time
  * lack of persistent caching of data

#### 2. Product Roadmap

Assuming that the end goal is along the lines of building a *Talent Scout* or *Butler Service*, useful improvements would include:
  * Time-series tracking, to see if a player endeavors to improve.
  * Extrapolated trajectories, to predict player improvement curve
  * Role-based comparison, to offer greater clarity and compartmentalization of a player's strengths.
  * Integrate matchups data, to better guess if the player has the potential to rise quickly in skill.
  * Machine-learning based suggestion engine, to offer more options like what other heroes the player could explore.

#### 3. API Preference

OpenDota API was chosen.
Of the two, the OpenDota API had clearer documentation and offered more control.
It also allowed fuzzy searching of player account ids based on username.

On the other hand, dota2api python library had codes already interpreted, which is convenient in understanding the responses from a human-readable perspective.

#### 4. Usefulness of recommendation engine

Currently, the engine merely retrieves the hero of which the player has the best win ratio.

Further improvements include suggesting based on:
  - desired roles
  - game modes
  - team configuration
  - heroes up against

These features would make it desirable as a "butler" service to optimize player win ratios.
