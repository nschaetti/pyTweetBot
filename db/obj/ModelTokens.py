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
from sqlalchemy import Column, BigInteger, String, Float, ForeignKey, Integer
from .Base import Base
from sqlalchemy.orm import relationship
from .Model import Model
from db.DBConnector import DBConnector


# Model's tokens
class ModelToken(Base):
    """
    Model's tokens
    """

    # Table name
    __tablename__ = "pytwb_model_tokens"

    # Fields
    token_id = Column(BigInteger, primary_key=True, autoincrement=True)
    token_model = Column(BigInteger, ForeignKey('pytwb_models.model_id'), nullable=False)
    token_text = Column(String(100), nullable=False)
    token_class = Column(Integer, nullable=False)
    token_prob = Column(Float, nullable=False, default=0.0)

    # Relationships
    model = relationship(Model)

    ##################################################
    # Functions
    ##################################################

    # Get token probabilities for a model
    @staticmethod
    def get_tokens_probabilities(model_name):
        """
        Get token probs for a model
        :param model_name: Model's name
        :return:
        """
        return DBConnector().get_session().query(Model).filter(ModelToken.token_model.model_name == model_name).all()
    # end get_tokens_probabilities

# end Statistic
