import random


class EmailTemplateProvider:
    """
    Provides the email templates specific for welcome emails.
    """

    ICONS = {
        'spinning': '🚲️',
        'pilates': '🤸‍♀️',
        'yoga': '🧘‍♀️',
        'shape': '💪',
        'health_exercise': '🏃‍♂️',
        'dynamic_design': '🎨',
        'feldenkrais': '🚶‍♂️',
        'bodypump': '🏋️‍♂️'
    }

    SUBJECTS = {
        'spinning': [
            'Ride Your Way to Fitness! 🚴',
            'Spinning Into Action! 🚴‍♂️ Ready?',
            'Your Spin Class Adventure Awaits! 🚴‍♀️',
            'Ride Your Way to Fitness! 🚴',
            'Spinning Into Action! 🚴‍♂️ Ready?',
            'Your Spin Class Adventure Awaits! 🚴‍♀️',
            'Pedal Power On! 🚴',
            'Get in the Spin Zone! 🚴',
            'Ride Like the Wind! 🚴',
            'Spinning: Where Fitness Meets Fun! 🚴',
            'Are You Ready to Ride? 🚴',
            'Spin It to Win It! 🚴',
            'Ride, Spin, Repeat! 🚴',
            'Spinning Magic in Every Ride! 🚴‍♂️',
            'Gear Up for the Spin Challenge! 🚴‍♀️',
            'Spin, Sweat, Succeed! 🚴',
            'Let the Wheels Turn and Burn! 🚴‍♂️',
            'Spinning: More than Just a Ride! 🚴‍♀️',
            'Experience the Spin Sensation! 🚴',
            'Join the Spin Revolution! 🚴‍♂️',
            'Pedal to the Peak of Fitness! 🚴‍♀️',
            'Elevate Every Spin Session! 🚴',
            'Commit to Spin, Commit to Win! 🚴‍♂️'
        ],
        'pilates': [
            'Pilates Party Alert! 🤸‍♀️ Are You In?',
            'Stretch, Strengthen, Succeed with Pilates! 🤸',
            'Pilates: Find Your Flex! 🤸‍♂️',
            'Pilates Power Hour! Are You Ready? 🤸',
            'Time to Flex Those Pilates Muscles! 🤸‍♀️',
            'Pilates and Perfection, A Match Made! 🤸',
            'Embrace the Pilates Pace! 🤸‍♂️',
            'Pilates: Balance, Strength, and Fun! 🤸',
            'Unlock Your Core with Pilates! 🤸‍♀️',
            'Pilates Pulse: Are You In? 🤸',
            'Pilates Perfection Awaits! 🤸',
            'Reach Your Peak with Pilates! 🤸‍♂️',
            'Pilates Power: Time to Shine! 🤸',
            'Get Flexy with Pilates! 🤸‍♀️',
            'Embrace the Power of Pilates! 🤸',
            'Pilates Pulse: Dive Deeper! 🤸‍♀️',
            'Pilates Passion in Every Pose! 🤸',
            'Feel the Pilates Power Within! 🤸‍♂️',
            'Recharge, Refresh, and Revive with Pilates! 🤸‍♀️',
            'Pilates: The Perfect Fitness Recipe! 🤸',
            'Challenge Your Limits with Pilates! 🤸‍♂️',
            'Pilates: Your Path to Poise and Power! 🤸‍♀️',
            'Strengthen from Within with Pilates! 🤸',
            'Pilates: Sculpt, Shape, Shine! 🤸‍♀️',
            'Experience Pilates Perfection! 🤸'
        ],
        'yoga': [
            'Ready to Find Your Zen? 🧘‍♀️',
            'Breathe, Stretch, Repeat with Yoga! 🧘',
            'Find Your Inner Peace with Yoga 🧘‍♂️',
            'Yoga: Your Journey to Serenity 🧘',
            'Join the Yoga Harmony Today! 🧘‍♀️',
            'Twist, Turn, and Transform with Yoga 🧘',
            'Unfold the Mysteries of Yoga 🧘‍♂️',
            'Awaken Your Spirit with Yoga 🧘',
            'Elevate Your Essence with Yoga 🧘‍♀️',
            'Dive Deep into Yoga Delight 🧘',
            'Explore Every Pose with Yoga 🧘‍♂️',
            'Yoga Vibes for the Soul 🧘',
            'Seek Balance. Seek Yoga. 🧘‍♀️',
            'Breathe in Positivity with Yoga 🧘',
            'Find Your Flex in Yoga 🧘‍♂️',
            'Flow with Grace in Yoga 🧘‍♂️',
            'Discover Tranquility with Every Pose 🧘',
            'Stretch Beyond Limits with Yoga 🧘‍♀️',
            'Soulful Sessions with Yoga 🧘',
            'Yoga: A Dance of Breath and Body 🧘‍♂️',
            'Embrace the Eternal Energy of Yoga 🧘',
            'Yoga: Where Mind, Body, and Spirit Unite 🧘‍♀️',
            'A Symphony of Serenity: Yoga 🧘',
            'Journey to the Heart of Yoga 🧘‍♂️',
            'Tap into Timeless Yoga Traditions 🧘'

        ],
        'shape': [
            'Shape Up and Show Off! 💪',
            'Get in the Best Shape of Your Life! 💪',
            'Discover the Shape of Fitness! 💪',
            'Get Your Shape On! Ready? 💪',
            'Shape: Where Strength Meets Style! 💪',
            'Shaping Dreams, One Workout at a Time! 💪',
            'Embrace the Shape Journey! 💪',
            'Shape Your Destiny with Fitness! 💪',
            'Elevate, Shape, Celebrate! 💪',
            'Shaping a Better Tomorrow! 💪',
            'Are You in Shape to Shape Up? 💪',
            'Craft Your Perfect Shape with Us! 💪',
            'The Art of Getting in Shape! 💪',
            'Fitness in Every Shape and Size! 💪',
            'Join the Shape Revolution Today! 💪',
            'Discover Your Dream Shape! 💪',
            'Shape Shift into Fitness! 💪',
            'Craft Your Ideal Contour! 💪',
            'Shape Goals? Let\'s Smash Them! 💪',
            'Step into the Shape Spotlight! 💪',
            'Emerge, Evolve, Shape Up! 💪',
            'Find Fitness in Every Form and Shape! 💪',
            'Reshape, Reimagine, Rekindle! 💪',
            'The Shape of Your Dreams is Within Reach! 💪',
            'Unlock the Ultimate Shape Shift! 💪'
        ],
        'health_exercise': [
            'Your Health. Your Move. Let\'s Go! 🏃‍♂️',
            'Embrace Health with Every Step! 🏃',
            'Where Health Meets Hustle 🏃‍♂️',
            'Move for Your Health, Stay for the Fun! 🏃',
            'Every Exercise is a Step Towards Health! 🏃‍♂️',
            'Are You Ready for a Health Boost? 🏃',
            'Step Up Your Health Game! 🏃‍♂️',
            'Exercise Today for a Healthier Tomorrow! 🏃',
            'Join the Health Hustle! 🏃‍♂️',
            'Run Towards Better Health! 🏃',
            'Health is Wealth, Let\'s Earn It! 🏃‍♂️',
            'Feel the Health in Every Move! 🏃',
            'Your Health Journey Starts Here! 🏃‍♂️',
            'Exercise, Energize, Elevate! 🏃',
            'Take the Health Route Today! 🏃‍♂️',
            'Champion Your Health Today! 🏃‍♂️',
            'Elevate Every Step with Health Exercise! 🏃',
            'Revitalize and Recharge: Choose Health! 🏃‍♂️',
            'Making Strides in Health and Fitness! 🏃',
            'Health: The Ultimate Endgame! 🏃‍♂️',
            'Get Fit, Get Healthy, Get Going! 🏃',
            'Ignite Your Health Revolution! 🏃‍♂️',
            'Strive for Health Excellence! 🏃',
            'Sweat, Smile, Repeat: The Health Mantra! 🏃‍♂️',
            'Journey to the Pinnacle of Health! 🏃'
        ],
        'dynamic_design': [
            'Designs That Move, Inspire, and Excite! 🎨',
            'Get Dynamic with Your Designs! 🎨',
            'Design Beyond Boundaries! 🎨',
            'Dive into Dynamic Designing 🎨',
            'Where Design Meets Dynamism 🎨',
            'Crafted with Precision, Delivered with Passion! 🎨',
            'Design Dreams, Dynamic Realities! 🎨',
            'Turn Ideas into Dynamic Masterpieces 🎨',
            'Experience the Power of Dynamic Designing 🎨',
            'Dynamic Design - The Future of Creativity 🎨',
            'Be Bold, Be Dynamic in Design 🎨',
            'Innovate, Illustrate, Elevate with Dynamic Design 🎨',
            'Crafting Designs That Speak Volumes! 🎨',
            'Dynamic Designs for the Modern World 🎨',
            'From Thought to Dynamic Creation 🎨',
            'Designs That Resonate and Radiate! 🎨',
            'The Future is Dynamic and Designed! 🎨',
            'Captivate with Every Creation! 🎨',
            'Make Waves in the World of Dynamic Design! 🎨',
            'The Art and Heart of Dynamic Design! 🎨',
            'Design Dreams, Dynamic Delivery! 🎨',
            'Turn Visions into Dynamic Visuals! 🎨',
            'Intricate Ideas, Dynamic Designs! 🎨',
            'The Dynamic Duo: Passion and Design! 🎨',
            'Innovation in Every Dynamic Illustration! 🎨'
        ],
        'feldenkrais': [
            'Discover Movement, Discover Yourself with Feldenkrais! 🚶‍♂️',
            'Embrace the Feldenkrais Flow! 🚶',
            'Movement Mastery with Feldenkrais 🚶‍♂️',
            'Unleash the Power of Feldenkrais Movement 🚶',
            'Find Your Feldenkrais Rhythm Today 🚶‍♂️',
            'Journey into the Art of Feldenkrais 🚶',
            'Discover, Move, Transform with Feldenkrais 🚶‍♂️',
            'Get in Tune with Feldenkrais Movements 🚶',
            'Unlocking Movement Potential with Feldenkrais 🚶‍♂️',
            'Feldenkrais: Every Move Counts 🚶',
            'Feel the Freedom with Feldenkrais Method 🚶‍♂️',
            'Dive into the Feldenkrais Experience 🚶',
            'Transformative Movements with Feldenkrais 🚶‍♂️',
            'Embark on a Feldenkrais Adventure 🚶',
            'Crafting Motion, One Move at a Time 🚶‍♂️',
            'Experience Euphoria with Feldenkrais! 🚶',
            'Fine-tune Your Movements with Feldenkrais! 🚶‍♂️',
            'Embark on the Feldenkrais Odyssey! 🚶',
            'Flawless Flow with Feldenkrais! 🚶‍♂️',
            'A Deep Dive into Dynamic Feldenkrais! 🚶',
            'Unearth the Feldenkrais Phenomenon! 🚶‍♂️',
            'Move, Morph, Master with Feldenkrais! 🚶',
            'Feldenkrais: The Frontier of Fitness! 🚶‍♂️',
            'Step into the Feldenkrais Finesse! 🚶',
            'Journey Through the Rhythms of Feldenkrais! 🚶‍♂️'
        ],
        'bodypump': [
            'Pump It Up and Get Ripped! 🏋️‍♂️',
            'Lift, Pump, Repeat! Are You Ready? 🏋️',
            'BodyPump: More than Just a Workout! 🏋️‍♂️',
            'Elevate Your Fitness Game with BodyPump 🏋️',
            'Strength, Stamina, BodyPump! 🏋️‍♂️',
            'Join the BodyPump Brigade Today! 🏋️',
            'Crafted for Strength: Dive into BodyPump! 🏋️‍♂️',
            'Get Pumped, Get Fit with BodyPump 🏋️',
            'Chisel Your Physique with BodyPump 🏋️‍♂️',
            'Unleashing Power with Every Pump 🏋️',
            'Transform, Uplift, and Pump It Up! 🏋️‍♂️',
            'Dedication, Perspiration, BodyPump! 🏋️',
            'Push Limits with the BodyPump Challenge 🏋️‍♂️',
            'Crafted to Pump, Built to Last! 🏋️',
            'Experience the Power of Pump! 🏋️‍♂️',
            'Elevate Every Lift with BodyPump! 🏋️‍♂️',
            'Master the Mechanics of BodyPump! 🏋️',
            'Push, Pump, Prevail! 🏋️‍♂️',
            'Reignite Your Passion with BodyPump! 🏋️',
            'Achieve Apex Athleticism with BodyPump! 🏋️‍♂️',
            'Lift Higher, Dive Deeper with BodyPump! 🏋️',
            'Power Up with the BodyPump Beat! 🏋️‍♂️',
            'The BodyPump Blueprint to Brilliance! 🏋️',
            'Pump, Power, Perform! 🏋️‍♂️',
            'The BodyPump Odyssey Awaits! 🏋️'
        ]
    }

    CONTENT = {
        "excitement_overload": {
            "body": "<p>Boom! 🎉 You're officially in for the <b>{lesson_type}</b> lesson! Are you as pumped as we are? 🚀 Ready to bring the house down? 🎸 Ready, set, go... Let's make this memorable!</p><p>Catch you on the flip side! ✌️</p>"
        },
        "casual_buddy": {
            "body": "<p>Guess who's joining the <b>{lesson_type}</b> party? Yep, it's you! 🎈 You think you're ready for this level of awesomeness? 😎 Just bring your enthusiasm, we've got the rest covered.</p><p>Later gator! 🐊</p>"
        },
        "chill_vibes": {
            "body": "<p>Hey there! So, you've decided to jump in on the <b>{lesson_type}</b> session? Cool choice. 😌 Let's take things easy and enjoy every moment.</p><p>Peace and love! ✨</p>"
        },
        "energetic_rush": {
            "body": "<p>Whoa! Get ready to turbocharge with the <b>{lesson_type}</b> lesson! 💥 Time to unleash that energy! 🌪️ Let's make waves!</p><p>Until then, keep shining! ☀️</p>"
        },
        "zen_master": {
            "body": "<p>Welcome, seeker. The path of <b>{lesson_type}</b> awaits you. 🍃 Embrace the journey and find your inner peace.</p><p>Stay tranquil. 🌙</p>"
        },
        "adventure_awaiting": {
            "body": "<p>The <b>{lesson_type}</b> adventure is calling you! 🌲 Are you packed and ready to explore? 🎒 Let's set off to the unknown.</p><p>Adventure on! 🗺️</p>"
        },
        "party_starter": {
            "body": "<p>Turn up the music! 🎶 The <b>{lesson_type}</b> party is about to start, and you're on the guest list! 🎊 Let's dance our hearts out!</p><p>Party hard! 🎉</p>"
        },
        "mystical_journey": {
            "body": "<p>The mystical world of <b>{lesson_type}</b> beckons you. 🌌 Embark on a journey of discovery and wonder.</p><p>May the stars guide you. 🌠</p>"
        },
        "comic_relief": {
            "body": "<p>Did you hear about the person who took a <b>{lesson_type}</b> lesson? They had a ball! 😂 Get ready for some laughs and good times!</p><p>Keep smiling! 😁</p>"
        },
        "space_odyssey": {
            "body": "<p>3... 2... 1... Blast off! 🚀 Your <b>{lesson_type}</b> journey is set to launch into the stratosphere! Dive into the cosmic vibes.</p><p>See you in space! 🪐</p>"
        },
        "jokester_jive": {
            "body": "<p>Why did the student choose the <b>{lesson_type}</b> lesson? To get to the other side, of course! 🐔 Prepare to LOL and ROFL during our session!</p><p>Stay hilarious! 😜</p>"
        },
        "quirky_quest": {
            "body": "<p>How many students does it take to start a <b>{lesson_type}</b> lesson? Just one... YOU! 🤪 Let's dive into this quirky adventure together!</p><p>Stay quirky! 🦄</p>"
        },
        "pun_tastic": {
            "body": "<p>It's <b>{lesson_type}</b> time! Or should I say... it's 'lesson' time you joined us! 😅 Prepare for puns and funs!</p><p>Pun you later! 🤓</p>"
        },
        "wacky_waves": {
            "body": "<p>Ever heard the one about the <b>{lesson_type}</b> student? Well, you're about to live it! 😆 Ready for some wacky experiences?</p><p>Stay wacky! 🌀</p>"
        },
        "giggle_galore": {
            "body": "<p>Knock, knock! Who's there? <b>{lesson_type}</b>. <b>{lesson_type}</b> who? <b>{lesson_type}</b> you glad you signed up for this? 😂</p><p>Keep giggling! 🤣</p>"
        },
        "silly_spirals": {
            "body": "<p>If you thought <b>{lesson_type}</b> was just another lesson, think again! We're all about the fun and the silly. 🤡 Let's spiral into silliness!</p><p>Silly on! 🎭</p>"
        },
        "funny_fiesta": {
            "body": "<p>Welcome to the <b>{lesson_type}</b> fiesta! 🎈 Where the only thing serious is... wait, there's nothing serious here! 😂</p><p>Stay fun-tastic! 🎪</p>"
        },
        "goofy_galaxy": {
            "body": "<p>Fasten your seatbelts! The <b>{lesson_type}</b> spaceship is headed to the Goofy Galaxy! 🌌 Expect out-of-this-world fun and maybe an alien joke or two!</p><p>Goof around! 👾</p>"
        },
        "lively_laughs": {
            "body": "<p>What's lively, fun, and full of laughs? Our <b>{lesson_type}</b> lesson! 🎭 Hop in and let's create some giggle-worthy moments!</p><p>Laugh on! 😹</p>"
        },
        "humor_haven": {
            "body": "<p>Welcome to the <b>{lesson_type}</b> humor haven! Where every moment is a meme and every lesson a laugh riot! 🤩</p><p>Stay chuckling! 😄</p>"
        },
        "laugh_lagoon": {
            "body": "<p>Dive into the <b>{lesson_type}</b> lagoon, where the laughs float and the fun never sinks! 🌊 Ready to make a splash?</p><p>Stay buoyant! 🏖️</p>"
        },
        "nutty_narrative": {
            "body": "<p>You've unlocked the <b>{lesson_type}</b> chapter in the nutty narrative of life! 📖 Ready for some plot twists and funny turns?</p><p>Go nuts! 🥳</p>"
        },
        "rofl_rollercoaster": {
            "body": "<p>All aboard the ROFL Rollercoaster! 🎢 The <b>{lesson_type}</b> highs and lows will leave you in stitches!</p><p>Roll on! 🌀</p>"
        },
        "haha_hangout": {
            "body": "<p>Welcome to the <b>{lesson_type}</b> hangout, where every second is a hoot and every minute is a meme! 😁</p><p>Hang tight! 🤘</p>"
        },
        "guffaw_grove": {
            "body": "<p>Step into the <b>{lesson_type}</b> grove and let's rustle up some riotous laughs! 🌳 Every leaf here is laced with laughter!</p><p>Branch out with fun! 🍃</p>"
        },
        "snicker_sphere": {
            "body": "<p>You're now entering the <b>{lesson_type}</b> sphere! A place where snickers sound and chuckles are found. 😄</p><p>Circle around with giggles! 🌐</p>"
        },
        "tickled_town": {
            "body": "<p>Welcome to Tickled Town! The <b>{lesson_type}</b> epicenter of all things funny. 🏘️ Ready for a tour de force of fun?</p><p>Stay tickled! 🤗</p>"
        },
        "whimsical_world": {
            "body": "<p>Unlock the gate to the whimsical world of <b>{lesson_type}</b>! 🗝️ Where every step is sprinkled with silliness!</p><p>Wander with whimsy! 🌍</p>"
        },
        "befuddled_boulevard": {
            "body": "<p>Strut down the <b>{lesson_type}</b> boulevard, where befuddlement is the order of the day! 🛣️ Ready for some comical confusion?</p><p>Stay bamboozled! 🤪</p>"
        },
        "chuckle_chamber": {
            "body": "<p>Welcome to the <b>{lesson_type}</b> chuckle chamber! Echoes of laughter and traces of mirth guaranteed! 🚪</p><p>Laugh it up! 😂</p>"
        },
        "giggle_galaxy": {
            "body": "<p>Prepare for liftoff into the <b>{lesson_type}</b> galaxy! 🌌 A realm where giggles light up the stars. Ready to shine?</p><p>Galaxy awaits! 🌟</p>"
        },
        "silly_station": {
            "body": "<p>All aboard the <b>{lesson_type}</b> express at Silly Station! 🚂 Choo-choo-choose to embrace the humor ahead!</p><p>Ride the fun wave! 🌊</p>"
        },
        "mirth_mountain": {
            "body": "<p>Scale the heights of <b>{lesson_type}</b> at Mirth Mountain! 🏔️ Every ascent is filled with amusement.</p><p>Peak the fun! ⛰️</p>"
        },
        "lark_lake": {
            "body": "<p>Dive deep into <b>{lesson_type}</b> Lark Lake! 🏞️ Where every ripple is a roar of laughter.</p><p>Stay afloat with joy! 🏊</p>"
        },
        "funny_farm": {
            "body": "<p>Yee-haw! Welcome to the <b>{lesson_type}</b> Funny Farm! 🐄 Where humor is harvested and chuckles are cultivated.</p><p>Farm some fun! 🌾</p>"
        },
        "jest_jungle": {
            "body": "<p>Roar into the <b>{lesson_type}</b> Jest Jungle! 🦁 Where the wild side of wit awaits.</p><p>Explore the exotic excitement! 🌴</p>"
        },
        "hilarity_harbor": {
            "body": "<p>Anchor down at <b>{lesson_type}</b> Hilarity Harbor! ⚓ Where waves of wit wash ashore.</p><p>Sail the sea of smiles! 🌊</p>"
        },
        "jocular_junction": {
            "body": "<p>Meet me at <b>{lesson_type}</b> Jocular Junction! 🚦 Where roads of rib-tickling tales intersect.</p><p>Drive down delight! 🚗</p>"
        },
        "whoopee_wilderness": {
            "body": "<p>Venture into the <b>{lesson_type}</b> Whoopee Wilderness! 🌲 A land where every echo is an exclamation of euphoria.</p><p>Trail the thrill! 🏞️</p>"
        },
        "lol_lobby": {
            "body": "<p>Step into the <b>{lesson_type}</b> LOL Lobby! 🏢 A space where smiles are the main service.</p><p>Linger in laughter! 😄</p>"
        }
    }

    LESSON_ICON_URLS = {
        'spinning': 'https://images.emojiterra.com/twitter/v14.0/512px/1f6b4-2642.png',
        'pilates': 'https://images.emojiterra.com/twitter/v14.0/256px/1f938-2642.png',
        'yoga': 'https://images.emojiterra.com/google/noto-emoji/unicode-15/color/256px/1f9d8.png',
        'shape': 'https://images.emojiterra.com/google/noto-emoji/unicode-15/color/svg/1f6b4-2642.svg',
        'health_exercise': 'https://images.emojiterra.com/google/noto-emoji/unicode-15/color/svg/1f6b4-2642.svg',
        'dynamic_design': 'https://images.emojiterra.com/google/noto-emoji/unicode-15/color/svg/1f6b4-2642.svg',
        'feldenkrais': 'https://images.emojiterra.com/google/noto-emoji/unicode-15/color/svg/1f6b4-2642.svg',
        'bodypump': 'https://images.emojiterra.com/google/noto-emoji/unicode-15/color/svg/1f6b4-2642.svg',
    }

    def __init__(self, lesson_type: str):
        """
        Initializes the email preparer with predefined icons, subjects, body content, and lesson type.
        :param lesson_type: The type of lesson for which the email will be prepared.
        """
        self.lesson_type = lesson_type
        self._subject = self._get_random_subject()
        self._icon = self.ICONS.get(self.lesson_type, '📧')
        self._body = self._get_random_body()

    def _get_random_subject(self) -> str:
        """
        Retrieve the subject of the email.
        :return: A randomly chosen subject for the initialized lesson type.
        """
        subjects_for_lesson = self.SUBJECTS.get(self.lesson_type, [])
        if subjects_for_lesson:
            return random.choice(subjects_for_lesson)
        return 'Your Lesson Adventure Awaits! '

    def _get_random_body(self) -> str:
        """
        Retrieve a random body content of the email based on the initialized lesson type.
        :return: The body content of the email.
        """
        style = random.choice(list(self.CONTENT.keys()))
        body_template = self.CONTENT.get(style, {}).get('body', "")
        return body_template.format(lesson_type=self.lesson_type.upper())

    @property
    def subject(self) -> str:
        """
        Retrieve the subject of the email.
        :return: The initialized subject for this instance.
        """
        return self._subject

    @property
    def body(self) -> str:
        """
        Retrieve the body content of the email.
        :return: The initialized body content for this instance.
        """
        return self._body

    @property
    def icon(self) -> str:
        """
        Retrieve the icon for the email.
        :return: The initialized icon for this instance.
        """
        return self._icon
