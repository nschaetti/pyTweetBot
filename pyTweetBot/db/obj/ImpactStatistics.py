#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File : Friend.py
# Description : pyTweetBot statistic class in the DB.
# Auteur : Nils Schaetti <n.schaetti@gmail.com>
# Date : 01.05.2017 17:59:05
# Lieu : Nyon, Suisse
#
# This file is part of the pyTweetBot.
# The pyTweetBot is a set of free software:
# you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyTweetBot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with pyTweetBar.  If not, see <http://www.gnu.org/licenses/>.
#

# Import
from sqlalchemy import Column, Integer, BigInteger, Enum, and_

from pyTweetBot.db import DBConnector
from .Base import Base


# Bot's impact statistics
class ImpactStatistic(Base):
    """
    Bot's impact statistics
    """

    # Table name
    __tablename__ = "pytwb_impact_statistics"

    # Fields
    impact_statistic_id = Column(BigInteger, primary_key=True, autoincrement=True)
    impact_statistic_week_day = Column(Enum('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday',
                                            'Sunday', name='week_day'), nullable=False)
    impact_statistic_hour = Column(Integer, nullable=False)
    impact_statistic_count = Column(Integer, nullable=False)

    ##################################################
    # Functions
    ##################################################

    # Impact statistics exists?
    @staticmethod
    def exists(week_day, hour):
        """
        Impact statistics exists?
        :param week_day:
        :param hour:
        :return:
        """
        return DBConnector().get_session().query(ImpactStatistic).filter(
            and_(ImpactStatistic.impact_statistic_week_day == week_day,
                 ImpactStatistic.impact_statistic_hour == hour)).count() > 0
    # end exists

    # Update
    @staticmethod
    def update(week_day, hour, count):
        """
        Update
        :param week_day:
        :param hour:
        :param count:
        :return:
        """
        DBConnector().get_session().query(ImpactStatistic).filter(
            and_(ImpactStatistic.impact_statistic_week_day == week_day,
                 ImpactStatistic.impact_statistic_hour == hour)).update({"impact_statistic_count": count})
    # end update

# end Statistic
