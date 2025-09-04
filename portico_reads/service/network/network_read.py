from sqlalchemy import select
from sqlalchemy.orm import selectinload, Session

from models.portico.pp_net import PPNetDict, PPNet


def get_networks(session:Session) -> list[PPNet]:
    """
    Retrieve a list of networks with a specified level of 5 and include their
    children's children relationships.

    This function executes a query to select networks from the database that have
    a level attribute equal to 5. It also loads the children of these networks,
    and recursively loads the children of the children, ensuring that all related
    data is efficiently fetched.

    :param session: SQLAlchemy database session used to execute the query.
    :type session: Session
    :return: A list of PPNet objects representing the networks with their nested
        children relationships.
    :rtype: list[PPNet]
    """
    stmt = (
        select(PPNet)
        .where(PPNet.level == 5)
        .options(
            selectinload(PPNet.children).selectinload(PPNet.children)
        )
    )

    networks: list[PPNet] = list(session.execute(stmt).unique().scalars().all())
    # networks = [result.to_dict() for result in results]
    return networks