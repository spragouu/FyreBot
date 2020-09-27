import aiosqlite
from discord.utils import get

#Grab data from DB
async def dbselect(db, sql, variables):
    db = await aiosqlite.connect(db)
    cursor = await db.execute(sql, variables)
    row = await cursor.fetchone()
    await cursor.close()
    await db.close()

    #If nothing is returned - Nothing happens
    if row is None:
        pass

    #If only a single result returned. It gets turned to it's proper Data Type
    elif len(row) == 1:
        try:
            row = int(row[0])
        except TypeError:
            row = str(row[0])
        except ValueError:
            row = str(row[0])

    #Otherwise it is returned as a list.
    else:
        row = list(row)

    return row

#Update data in the DB
async def dbupdate(db, sql, variables):
    db = await aiosqlite.connect(db)
    cursor = await db.execute(sql, variables)
    await db.commit()
    await cursor.close()
    await db.close()

#Check if data is present in the DB
async def is_in_database(*, sql):
    check = await dbselect('main.db', sql, ())
    if check is None:
        return False
    return True

async def getLogChannel(guild):
        logChannelDB = await dbselect('main.db', 'SELECT log_channel FROM servers WHERE server=?', (guild.id,))
        logChannel = get(guild.channels, id = logChannelDB)
        if logChannelDB is None:
            return
        elif logChannel is None:
            return
        else:
            return logChannel